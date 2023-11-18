from pydantic import BaseModel, constr
from typing import List, Union


class Source(BaseModel):
    source_type: str
    content: Union[str, bytes]


class TaskData(BaseModel):
    id_worker: str
    domain: str
    input_words: str  # comma-separated words
    task: str  ## tasks : words, definition, synonyms, antonyms, examples, historical_events, historical_figures.
    sources: List[Source]  ## Change it to List[Source]
