from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    hashed_password: str

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    hashed_password: str
    create_at: datetime
    update_at: datetime
    
    class Config:
        from_attributes = True
