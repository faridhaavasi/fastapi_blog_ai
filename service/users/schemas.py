from pydantic import BaseModel, Field
from users.models import UserModel

class UserLoginSchema(BaseModel):
    email : str = Field(..., description="email of the user")
    password : str = Field(..., description="password of the user")



class UserStartRegisterSchema(BaseModel):
    email: str = Field(..., description="email of the user")