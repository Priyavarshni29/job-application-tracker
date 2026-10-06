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
    is_archived: bool

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str