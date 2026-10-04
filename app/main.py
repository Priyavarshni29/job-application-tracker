from fastapi import FastAPI

app = FastAPI(
    title="Job Application Tracker",
    description="REST API for tracking job applications",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Job Application Tracker API is running"
    }