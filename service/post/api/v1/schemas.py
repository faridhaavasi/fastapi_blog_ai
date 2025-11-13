from pydantic import BaseModel, Field


class UserCreatePostSchema(BaseModel):
    title: str = Field(..., description='please enter your post\'s title')
    description: str = Field(..., description='please enter your post\'s description')

class UserUpdatePostSchema(BaseModel):
    title: str = Field(description='please enter your post\'s title')
    description: str = Field(description='please enter your post\'s description')

class GetAllPostSchema(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    tags: list[str]

class UserCreateCommentSchema(BaseModel):
    comment: str = Field(..., description='please enter your comment')