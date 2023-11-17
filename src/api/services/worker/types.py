from pydantic import BaseModel, constr
from typing import List


class TaskData(BaseModel):
    id_worker: str
    domain: str
    input_words: str# comma-separated words
    task: str ## tasks : words, definition, synonyms, antonyms, examples, historical_events, historical_figures. 
    sources: List[str] ## Change it to List[Source]
