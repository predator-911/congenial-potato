from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class AuthRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=10, max_length=256)

class UserOut(BaseModel):
    id: str
    email: str
    created_at: datetime

class AuthResponse(BaseModel):
    user: UserOut
