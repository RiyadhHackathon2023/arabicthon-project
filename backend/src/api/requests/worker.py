from pydantic import BaseModel, constr
from typing import Optional, List


class WorkerData(BaseModel):
    name: str
    source_ids: List[str]
    input_words: str  # comma-separated words
    task: str  ## tasks : words, definition, synonyms, antonyms, examples, historical_events, historical_figures.
    domain: str
    description: str


class RelationUpdateRequest(BaseModel):
    id_relation: str
    status: str