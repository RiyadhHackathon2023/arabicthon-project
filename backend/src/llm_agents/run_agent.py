import time
from src.api.services.worker.types import TaskData, Source, WorkerTaskEnum
from src.llm_agents.pipelines.generate_definitions import generate_definitions
from src.llm_agents.pipelines.generate_events import generate_events
from src.llm_agents.pipelines.generate_places import generate_places
from src.llm_agents.pipelines.generate_terms import generate_terms




def run_agent(data: TaskData):
    if data.task == str(WorkerTaskEnum.Definition):
        print("Running agent with task 3: ", data.task)
        return generate_definitions(
            worker_id=data.id_worker,
            sources=[{
                "type": source.source_type,
                "content": source.content
            } for source in data.sources],
            domain=data.domain,
            words=data.input_words.split(sep=','),
            
        )
    elif data.task == str(WorkerTaskEnum.HisEvents):
        print("Running agent with task 2: ", data.task)
        return generate_events(
            worker_id=data.id_worker,
            sources=[{
                "type": source.source_type,
                "content": source.content
            } for source in data.sources],
            domain=data.domain,
            task=data.task,
        )
    elif data.task == str(WorkerTaskEnum.Places):
        print("Running agent with task 3: ", data.task)
        return generate_places(
            worker_id=data.id_worker,
            sources=[{
                "type": source.source_type,
                "content": source.content
            } for source in data.sources],
            domain=data.domain,
            task=data.task,
            
        )
    elif data.task == str(WorkerTaskEnum.KeyTerms):
        print("Running agent with task 4: ", data.task)
        return generate_terms(
            worker_id=data.id_worker,
            sources=[{
                "type": source.source_type,
                "content": source.content
            } for source in data.sources],
            domain=data.domain,
            task=data.task,
        )
    return 'OK'