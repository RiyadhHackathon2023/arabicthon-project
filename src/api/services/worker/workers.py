
from ....db.models import WorkerStatusEnum
from ....llm_agents.run_agent import run_agent
from rq import Queue, Worker as RqWorker
from rq.job import Job
from redis import Redis

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
        return self.queue.enqueue_call(
            run_agent,
            args=[self.data],
        )