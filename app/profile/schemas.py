from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ProfileCreate(BaseModel):
    study_method: str
    main_motivation: str


class ProfileResponse(BaseModel):
    id: UUID
    study_method: str
    main_motivation: str
    create_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True
