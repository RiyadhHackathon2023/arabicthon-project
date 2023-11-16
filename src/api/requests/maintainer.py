from pydantic import BaseModel, constr
from typing import Optional


class CreateMaintainerRequest(BaseModel):
    name: str
    email: str
    password: str



class UpdateMaintainerRequest(CreateMaintainerRequest):
    pass