from pydantic import BaseModel, constr
from ...db.models import SourceTypeEnum


class LoginRequest(BaseModel):
    email: str
    password: str
