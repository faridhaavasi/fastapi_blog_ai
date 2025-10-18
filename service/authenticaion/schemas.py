from pydantic import BaseModel, Field, EmailStr

from typing import Dict


class SetEmailInputSchema(BaseModel):
    email : EmailStr = Field(..., description="Enter your email")