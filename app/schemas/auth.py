from pydantic import BaseModel


class SignUpRequest(BaseModel):
    email: str
    password: str


class SignUpResponse(BaseModel):
    id: int
    email: str
    token: str