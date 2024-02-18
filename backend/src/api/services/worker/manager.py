from redis import Redis
from rq import Queue, Worker as RqWorker
from .workers import Worker
from ....db.models import WorkerModel, WorkerStatusEnum, WorkerSourceModel, SourceModel
from ....db.session import get_session
from ..utils.schedule import interval
from ...requests.worker import WorkerData, RelationUpdateRequest
from datetime import datetime
import enum
import json
import os
from typing import List
from ..responses.service_response import ServiceResponse
from src.neo4j_db.neo4j_connection import get_neo4j_connection
from .types import WorkerTaskEnum
import logging
import uuid

logger = logging.getLogger(__name__)

from rq.registry import (
    DeferredJobRegistry,
    FailedJobRegistry,
    FinishedJobRegistry,
    StartedJobRegistry,
    CanceledJobRegistry,
    ScheduledJobRegistry,
)


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class WorkerManagerStatus(enum.Enum):
    Running = "Running"
    Stopped = "Stopped"


class WorkerManager(metaclass=SingletonMeta):

    def __init__(self) -> None:
        print('WorkerManager Init')
        self.redis_conn = Redis(
            host=os.getenv('REDIS_HOST') or "127.0.0.1",
            port=os.getenv('REDIS_PORT') or 6379,
        )
        self.queue = Queue(connection=self.redis_conn)
        self.rq_worker = RqWorker([self.queue],
                                  connection=self.redis_conn,
                                  name=f'backend-{uuid.uuid4().hex}')

        self.rq_worker_status = WorkerManagerStatus.Stopped
        self.update_jobs_status()

    ## This function is called in fast api background task
    def start_rq_worker(self):
        if self.rq_worker_status != WorkerManagerStatus.Running:
            try:
                self.rq_worker.work()
            except Exception as e:
                print(e)
            self.rq_worker_status = WorkerManagerStatus.Running

    async def spawn_worker(self, data: WorkerData):
        ## Prepare worker data
        print('Spawning new worker')
        ## Create it
        w = Worker(self.queue, self.redis_conn, data)
        ## Run
        await w.run()

    @interval(every=5)
    def update_jobs_status(self):
        # print("Update Jobs Status")
        # if self.queue.is_empty():
        #     print('Queue is empty, no updates')
        #     return
        self.update_pending_workers()
        self.update_running_workers()
        self.update_completed_workers()
        self.update_failed_workers()
        self.update_canceled_workers()

    def update_completed_workers(self):
        completed_workers_ids = self.get_completed_workers()
        session = get_session()
        session.begin()
        for wid in completed_workers_ids:
            worker:WorkerModel  = session\
                .query(WorkerModel)\
                .filter(WorkerModel.worker_id == wid)\
                .first()
            #TODO: Check if state change and emit to front
            if worker:
                prev_status = worker.worker_status
                worker.worker_status = WorkerStatusEnum.Completed
                if prev_status != worker.worker_status:
                    ## Status change, emit
                    print(
                        f'Worker {wid} changed status from {str(prev_status)} to {WorkerStatusEnum.Completed.value}'
                    )
                    self.redis_conn.publish(
                        channel='workers:events',
                        message=json.dumps({
                            'worker_id':
                            worker.worker_id,
                            'prev_status':
                            str(prev_status),
                            'current_status':
                            WorkerStatusEnum.Completed.value
                        }))
                    worker.end_date = datetime.now()
                    session.add(worker)
        try:
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

    def update_pending_workers(self):
        pending_workers_ids = self.get_pending_workers()
        session = get_session()
        session.begin()
        for wid in pending_workers_ids:
            worker:WorkerModel  = session\
                .query(WorkerModel)\
                .filter(WorkerModel.worker_id == wid)\
                .first()
            #TODO: Check if state change and emit to front
            if worker:
                prev_status = worker.worker_status
                worker.worker_status = WorkerStatusEnum.Pending
                if prev_status != worker.worker_status:
                    ## Status change, emit
                    print(
                        f'Worker {wid} changed status from {str(prev_status)} to {WorkerStatusEnum.Pending.value}'
                    )
                    self.redis_conn.publish(channel='workers:events',
                                            message=json.dumps({
                                                'worker_id':
                                                worker.worker_id,
                                                'prev_status':
                                                str(prev_status),
                                                'current_status':
                                                WorkerStatusEnum.Pending.value
                                            }))
                    session.add(worker)
        try:
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

    def update_running_workers(self):
        running_workers_ids = self.get_running_workers()
        session = get_session()
        session.begin()
        for wid in running_workers_ids:
            worker:WorkerModel  = session\
                .query(WorkerModel)\
                .filter(WorkerModel.worker_id == wid)\
                .first()
            #TODO: Check if state change and emit to front
            if worker:
                prev_status = worker.worker_status
                worker.worker_status = WorkerStatusEnum.Running
                if prev_status != worker.worker_status:
                    ## Status change, emit
                    print(
                        f'Worker {wid} changed status from {str(prev_status)} to {WorkerStatusEnum.Running.value}'
                    )
                    self.redis_conn.publish(channel='workers:events',
                                            message=json.dumps({
                                                'worker_id':
                                                worker.worker_id,
                                                'prev_status':
                                                str(prev_status),
                                                'current_status':
                                                WorkerStatusEnum.Running.value
                                            }))
                    session.add(worker)
        try:
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

    def update_failed_workers(self):
        failed_workers_ids = self.get_failed_workers()
        session = get_session()
        session.begin()
        for wid in failed_workers_ids:
            worker:WorkerModel  = session\
                .query(WorkerModel)\
                .filter(WorkerModel.worker_id == wid)\
                .first()
            #TODO: Check if state change and emit to front
            if worker:
                prev_status = worker.worker_status
                worker.worker_status = WorkerStatusEnum.Failed
                if prev_status != worker.worker_status:
                    ## Status change, emit
                    print(
                        f'Worker {wid} changed status from {str(prev_status)} to {WorkerStatusEnum.Failed.value}'
                    )
                    self.redis_conn.publish(channel='workers:events',
                                            message=json.dumps({
                                                'worker_id':
                                                worker.worker_id,
                                                'prev_status':
                                                str(prev_status),
                                                'current_status':
                                                WorkerStatusEnum.Failed.value
                                            }))
                    worker.end_date = datetime.now()
                    session.add(worker)
        try:
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

    def update_canceled_workers(self):
        canceled_workers_ids = self.get_canceled_workers()
        session = get_session()
        session.begin()
        for wid in canceled_workers_ids:
            worker:WorkerModel  = session\
                .query(WorkerModel)\
                .filter(WorkerModel.worker_id == wid)\
                .first()
            #TODO: Check if state change and emit to front
            if worker:
                prev_status = worker.worker_status
                worker.worker_status = WorkerStatusEnum.Canceled
                if prev_status != worker.worker_status:
                    print(
                        f'Worker {wid} changed status from {str(prev_status)} to {WorkerStatusEnum.Canceled.value}'
                    )
                    ## Status change, emit
                    self.redis_conn.publish(channel='workers:events',
                                            message=json.dumps({
                                                'worker_id':
                                                worker.worker_id,
                                                'prev_status':
                                                str(prev_status),
                                                'current_status':
                                                WorkerStatusEnum.Canceled.value
                                            }))
                    worker.end_date = datetime.now()
                    session.add(worker)
        try:
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

    def get_completed_workers(self) -> list[str]:
        registry = FinishedJobRegistry(name=self.queue.name,
                                       connection=self.queue.connection,
                                       job_class=self.queue.job_class,
                                       serializer=self.queue.serializer)
        return registry.get_job_ids()

    def get_pending_workers(self) -> list[str]:
        deferred_registry = DeferredJobRegistry(
            name=self.queue.name,
            connection=self.queue.connection,
            job_class=self.queue.job_class,
            serializer=self.queue.serializer)
        scheduled_registry = ScheduledJobRegistry(
            name=self.queue.name,
            connection=self.queue.connection,
            job_class=self.queue.job_class,
            serializer=self.queue.serializer)
        return deferred_registry.get_job_ids(
        ) + scheduled_registry.get_job_ids()

    def get_running_workers(self) -> list[str]:
        stareted_registry = StartedJobRegistry(
            name=self.queue.name,
            connection=self.queue.connection,
            job_class=self.queue.job_class,
            serializer=self.queue.serializer)
        return stareted_registry.get_job_ids()

    def get_failed_workers(self) -> list[str]:
        failed_registry = FailedJobRegistry(name=self.queue.name,
                                            connection=self.queue.connection,
                                            job_class=self.queue.job_class,
                                            serializer=self.queue.serializer)
        return failed_registry.get_job_ids()

    def get_canceled_workers(self) -> list[str]:
        canceled_registry = CanceledJobRegistry(
            name=self.queue.name,
            connection=self.queue.connection,
            job_class=self.queue.job_class,
            serializer=self.queue.serializer)
        return canceled_registry.get_job_ids()

    ### API related services
    async def get_workers_by_id(self, worker_id: str):
        session = get_session()
        worker_db: List[WorkerModel] = session.query(WorkerModel).order_by(WorkerModel.start_date.desc())\
            .filter(WorkerModel.worker_id == worker_id)\
            .first()
        wsources_db: List[WorkerSourceModel] = session.query(WorkerSourceModel).filter(WorkerSourceModel.worker_id == worker_id).all()
        
        if worker_db:
            ## Fetch neo4j connection
            conn = get_neo4j_connection()
            outputs = None
            rate = 0
            if worker_db.task == str(WorkerTaskEnum.Definition):
                outputs, rate = conn.get_definitions(
                    worker_id=worker_db.worker_id)
            else:
                outputs, rate = conn.get_words(
                    worker_id=worker_db.worker_id)
                

            result = worker_db.tojson()
            result['outputs'] = outputs
            result['completion'] = rate
            result["sources"] = []
            
            if wsources_db:
                
                result["sources"] = [session.query(SourceModel).filter(SourceModel.source_id == ws_db.source_id).first().tojson() for ws_db in wsources_db]

            return ServiceResponse(response_status='success',
                                   data=result,
                                   http_code=200,
                                   message='')
        return ServiceResponse(response_status='error',
                               data=None,
                               http_code=404,
                               message='Worker not found')

    async def get_workers(self):
        session = get_session()
        workers_db: List[WorkerModel] = session.query(WorkerModel).order_by(
            WorkerModel.start_date.desc()).all()
        if workers_db:
            conn = get_neo4j_connection()

            data = []
            for worker_db in workers_db:
                outputs = None
                rate = 0
                if worker_db.task == str(WorkerTaskEnum.Definition):
                    outputs, rate = conn.get_definitions(
                        worker_id=worker_db.worker_id)
                else:
                    outputs, rate = conn.get_words(
                        worker_id=worker_db.worker_id)

                result = worker_db.tojson()
                result['outputs'] = outputs
                result['completion'] = rate
                result["sources"] = []
                wsources_db: List[WorkerSourceModel] = session.query(WorkerSourceModel).filter(WorkerSourceModel.worker_id == worker_db.worker_id).all()
                if wsources_db:
                    result["sources"] = [session.query(SourceModel).filter(SourceModel.source_id == ws_db.source_id).first().tojson() for ws_db in wsources_db]

                data.append(result)
            session.close()
            return ServiceResponse(response_status='success',
                                   data=data,
                                   http_code=200,
                                   message='')
        session.close()
        return ServiceResponse(response_status='success',
                               data=[],
                               http_code=200,
                               message='')

    async def update_relation_output(self, update_data: RelationUpdateRequest):
        conn = get_neo4j_connection()
        result = conn.change_has_output_status(
            has_output_id=update_data.id_relation,
            new_status=update_data.status)
        return ServiceResponse(
            response_status='success' if result else 'error',
            data='',
            message='Updated' if result else 'Error occured',
            http_code=200 if result else 500)
