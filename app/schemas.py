from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ApplicationBase(BaseModel):
    company: str
    role: str
    status: str = "Applied"
    application_date: Optional[date] = None
    oa_date: Optional[date] = None
    interview_date: Optional[date] = None
    package: Optional[str] = None
    notes: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationResponse(ApplicationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
