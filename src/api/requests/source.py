from pydantic import BaseModel, constr


class LoginRequest(BaseModel):
    email: str
    password: str