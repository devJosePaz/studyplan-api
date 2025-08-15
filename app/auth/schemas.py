from pydantic import BaseModel
from uuid import UUID
import datetime

class UserCreate(BaseModel):
    email: str
    hashed_password: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    hashed_password: str
    create_at: datetime
    update_at: datetime
    
    class Config:
        from_attributes = True
