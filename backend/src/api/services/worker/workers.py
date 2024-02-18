from ....db.models import WorkerStatusEnum
from ....llm_agents.run_agent import run_agent
from rq import Queue, Worker as RqWorker
from rq.job import Job
from redis import Redis
from ...requests.worker import WorkerData
from ....db.models import WorkerModel, WorkerStatusEnum, SourceModel, SourceTypeEnum, WorkerSourceModel
from ....db.session import get_session
from rq.job import Job, JobStatus
import json
from typing import Union
from .types import TaskData, Source
from ..sources import get_sources_by_type
import uuid
from ....storage_manager.storage import get_swift_connection


def on_success(job: Job, connection, result, *args, **kwargs):
    print("on_success", job.ended_at, *args)
    # TODO: Mark worker as Completed


def on_failure(job, connection, type, value, traceback):
    print("on_failure", job)
    # TODO: Mark worker as Failed


def on_stopped(job, connection):
    print("on_failure", job)
    # TODO: Mark worker as Canceled


class Worker:

    def __init__(self, queue: Queue, redis: Redis, data: any):
        # Tell RQ what Redis connection to use
        self.queue = queue  # no args implies the default queue
        self.data = data
        self.status = WorkerStatusEnum.Pending
        self.job: Union[Job, None] = None
        self.job_id = uuid.uuid4().hex

    async def run(self):
        print('Run ...')
        task_data = self.worker_data_to_task_data(self.data)
        print(task_data)
        self.job = self.queue.enqueue_call(
            run_agent,
            args=[task_data],
            timeout=2 * 3600,  # 2h max
            job_id=self.job_id,
        )
        

        w = self.commit_new_worker(self.job, self.data)
        self.queue.connection.publish(channel='workers:events',
                                      message=json.dumps({
                                          'worker_id':
                                          w["worker_id"],
                                          'prev_status':
                                          None,
                                          'current_status':
                                          w["worker_status"]
                                      }))
        return self.job

    def commit_new_worker(self, job: Job, data: WorkerData):
        session = get_session()
        w = WorkerModel(
            worker_id=job.get_id(),
            worker_name=data.name,
            worker_description=data.description,
            worker_status=self.map_job_status_worker_status(job),
            task=data.task,
            domain=data.domain,
        )
        ## Create worker sources
        worker_dto = w.tojson()
        session.add(w)
        for source_id in data.source_ids:
            ws = WorkerSourceModel(
                worker_id=job.get_id(),
                source_id=source_id
            )
            session.add(ws)

        session.commit()
        session.close()
        return worker_dto

    def map_job_status_worker_status(self, status: JobStatus):
        if status == JobStatus.CANCELED:
            return WorkerStatusEnum.Canceled
        if status == JobStatus.FAILED:
            return WorkerStatusEnum.Failed
        if status == JobStatus.FINISHED:
            return WorkerStatusEnum.Completed
        if status == JobStatus.STARTED:
            return WorkerStatusEnum.Running
        return WorkerStatusEnum.Pending

    def worker_data_to_task_data(self, data: WorkerData):
        ## Fetch sources
        session = get_session()
        sources_db = session.query(SourceModel).filter(
            SourceModel.source_id.in_(data.source_ids)).all()
        if sources_db:
            ## Found data
            task_data = TaskData(
                domain=data.domain,
                id_worker=self.job_id,
                input_words=data.input_words,
                sources=[self.get_source(source) for source in sources_db],
                task=data.task)

            session.close()
            return task_data
        session.close()

    def get_source(self, source: SourceModel):
        # print(source)
        if source.source_type == SourceTypeEnum.Url or source.source_type == SourceTypeEnum.Wikipedia:
            return Source(source_type=str(source.source_type),
                          content=source.source_url)
        ### Read data
        swift = get_swift_connection()
        f_name = source.source_name
        f_path = f'{f_name}_{source.source_id}'
        swift = get_swift_connection()
        try:
            header, obj = swift.connection.get_object('documents', f_path)
            return Source(source_type=str(source.source_type), content=obj)
        except:
            return None
        finally:
            swift.connection.close()