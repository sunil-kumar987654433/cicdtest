from datetime import datetime
import uuid

from pydantic import BaseModel, EmailStr, field_validator, model_validator

class UserBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    password1: str
    password2: str

    @model_validator(mode='after')
    def varify_password(self):
        if self.password1 != self.password2:
            raise ValueError("Both password must be equal")
        if len(self.password2) < 4:
            raise ValueError("Password length must be or equal to 4")
        return self
    
class UserResponse(UserBase):
    id: int
    key: uuid.UUID
    is_active: bool
    is_verified: bool
    user_role: str
    profile_image: str
    hashed_password: str | None = None
    created_at: datetime
    updated_at: datetime





