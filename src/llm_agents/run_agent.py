import time
from src.api.services.worker.types import TaskData, Source
from src.llm_agents.pipelines.generate_definitions import generate_definitions


def run_agent(data: TaskData):
    print("Running agent with data: ", )
    # return generate_definitions(
    #     worker_id=data.id_worker,
    #     sources=[{
    #         "type": source.source_type,
    #         "content": source.content
    #     } for source in data.sources],
    #     domain=data.domain,
    #     words=data.input_words.split(sep=','),
    # )
    time.sleep(5)
    return data