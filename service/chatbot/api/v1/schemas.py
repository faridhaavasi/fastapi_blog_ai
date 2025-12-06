# Pydantic
from pydantic import BaseModel, Field


class GetAllMassageSchema(BaseModel):
    role : str
    message : str


class UserSendMassageSchema(BaseModel):
    message : str = Field(..., description='please enter your message')