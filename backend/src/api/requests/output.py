from pydantic import BaseModel

class UpdateWordRequest(BaseModel):
    relation_id: str
    worker_id: str
    word: str



class UpdateDefinitionRequest(BaseModel):
    relation_id: str
    worker_id: str
    definition: str