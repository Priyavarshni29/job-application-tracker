from datetime import date
from sqlalchemy import Column, Integer, String, Date, Boolean
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)

    company = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="Applied")

    application_date = Column(Date, default=date.today)
    oa_date = Column(Date, nullable=True)
    interview_date = Column(Date, nullable=True)

    package = Column(String(50), nullable=True)
    notes = Column(String(500), nullable=True)

    is_archived = Column(Boolean, nullable=False, default=False)