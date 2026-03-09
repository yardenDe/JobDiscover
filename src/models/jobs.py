from datetime import datetime
from pydantic import BaseModel, Field

class JobModel(BaseModel):
    job_id: str = Field(...)
    title: str
    company: str
    link: str
    location: str = "Israel"
    discovered_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True