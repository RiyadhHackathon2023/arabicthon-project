
from ....db.models import WorkerStatusEnum
from ....llm_agents.run_agent import run_agent
from rq import Queue, Worker as RqWorker
from rq.job import Job
from redis import Redis
from ...requests.worker import WorkerData
from ....db.models import WorkerModel, WorkerStatusEnum
from ....db.session import get_session
from rq.job import Job, JobStatus
import json



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
        self.job: Job | None = None

    async def run(self):
        print('Run ...')
        self.job =  self.queue.enqueue_call(
            run_agent,
            args=[self.data],
        )
        
        w = self.commit_new_worker(self.job, self.data)
        self.queue.connection.publish(
                    channel='workers:events',
                    message=json.dumps({
                            'worker_id': w["worker_id"],
                            'prev_status': None,
                            'current_status': w["worker_status"]
                    })
        )
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
        worker_dto = w.tojson()
        session.add(w)
        session.commit()
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
        return ""