from pydantic import BaseModel, Field
from typing import Optional


class TokenRequest(BaseModel):
    username: str = Field(..., description="Username ")
    password: str = Field(..., description="Password")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInDB(BaseModel):
    user_id: int
    username: str
    is_active: bool = True
