from pydantic import BaseModel , EmailStr


class SetEmailSchema(BaseModel):
    email_addr : EmailStr