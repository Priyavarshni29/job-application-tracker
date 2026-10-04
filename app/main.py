from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routes.applications import router as applications_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Application Tracker",
    description="REST API for tracking job applications",
    version="1.0.0"
)

app.include_router(applications_router)


@app.get("/")
def root():
    return {
        "message": "Job Application Tracker API is running"
    }