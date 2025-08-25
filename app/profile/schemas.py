from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ProfileCreate(BaseModel):
    user_id: UUID
    learning_style: str
    challenge_tolerance: str
    focus: str
    study_resilience: str
    

class ProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    learning_style: str
    challenge_tolerance: str
    focus: str
    study_resilience: str
    
    create_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True
