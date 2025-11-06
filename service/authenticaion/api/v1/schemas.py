from pydantic import BaseModel, Field, EmailStr, model_validator

from typing import Dict


class SetEmailInputSchema(BaseModel):
    email : EmailStr = Field(..., description="Enter your email")



class RegisterFinallySchema(BaseModel):
    token: str = Field(..., description="Enter refresh token")
    password: str = Field(..., description="Enter password")
    confer_password: str = Field(..., description="Enter confirm password")

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.confer_password:
            raise ValueError("Passwords do not match")
        return self


class SetTokenSchema(BaseModel):
    email : EmailStr = Field(..., description="Please enter your mail")
    password : EmailStr = Field(..., description="Please enter your mail")
