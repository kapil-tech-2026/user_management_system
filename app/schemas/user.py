from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: Literal["user", "admin"]

    model_config = ConfigDict(from_attributes=True)
