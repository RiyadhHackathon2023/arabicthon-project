from pydantic import BaseModel, constr
from typing import List, Union
import enum


class Source(BaseModel):
    source_type: str
    content: Union[str, bytes]


class TaskData(BaseModel):
    id_worker: str
    domain: str
    input_words: str  # comma-separated words
    task: str  ## tasks : words, definition, synonyms, antonyms, examples, historical_events, historical_figures.
    sources: List[Source]  ## Change it to List[Source]


class WorkerTaskEnum(enum.Enum):
    Definition = "definition"
    Synonyms = "synonyms"
    Antonyms = "antonyms"
    HisEvents = "his_events"
    KeyTerms = "key_terms"
    Places = "places"


    def __str__(self):
        return str(self.value)