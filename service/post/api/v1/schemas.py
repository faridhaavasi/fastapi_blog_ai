from pydantic import BaseModel, Field


class UserCreatePostSchema(BaseModel):
    title: str = Field(..., description='please enter your post\'s title')
    description: str = Field(..., description='please enter your post\'s description')