from redis import Redis
from rq import Queue, Worker as RqWorker
from .workers import Worker
from ....db.models import WorkerModel, WorkerStatusEnum
from ....db.session import get_session
from ..utils.schedule import interval
import schedule
import enum

import uuid
from rq.job import Job, JobStatus
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
        print('init')
        self.redis_conn = Redis()
        self.queue = Queue(connection=self.redis_conn)
        
        self.rq_worker = RqWorker([self.queue], connection=self.redis_conn, name='backend')
        self.rq_worker_status = WorkerManagerStatus.Stopped
    ## This function is called in fast api background task
    def start_rq_worker(self):
        if self.rq_worker_status != WorkerManagerStatus.Running:
            self.rq_worker.work()
            self.rq_worker_status = WorkerManagerStatus.Running
        
    async def spawn_worker(self, data):
        ## Prepare worker data
        print('Spawning new worker')
        ## Create it
        w = Worker(self.queue, self.redis_conn, data)
        ## Add worker to state
        job = await w.run()
        ## Add to db

    def commit_new_worker(self, job: Job, data):
        session = get_session()
        w = WorkerModel(
            worker_id=job.get_id(),
            worker_name=data.name,
            worker_description=data.description,
            worker_status=self.map_job_status_worker_status(job),
        )
        session.add(w)
        session.commit()
    
    @interval(every=2)
    def update_jobs_status(self):
        print("Hii")

    def cancel_worker():
        pass

    def get_completed_workers():
        return FinishedJobRegistry.get_job_ids()
        
    def get_pending_workers():
        pass

    def get_running_workers():
        pass

    def get_failed_workers():
        pass

    def get_canceled_workers():
        pass

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