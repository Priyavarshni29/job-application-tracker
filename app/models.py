from datetime import date
from sqlalchemy import Column, Integer, String, Date
from app.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="Applied")
    application_date = Column(Date, default=date.today)
    oa_date = Column(Date, nullable=True)
    interview_date = Column(Date, nullable=True)
    package = Column(String(50), nullable=True)
    notes = Column(String(500), nullable=True)