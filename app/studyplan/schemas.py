from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class StudyPlanCreate(BaseModel):
    theme: str
    theme_level: str
    week_time: int
    objective: str

class StudyPlanResponse(StudyPlanCreate):
    id: UUID
    user_id: UUID
    theme: str
    theme_level: str
    week_time: int
    objective: str

    create_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True



