from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Application

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/")
def get_analytics(db: Session = Depends(get_db)):
    total = db.query(func.count(Application.id)).scalar()

    status_counts = (
        db.query(
            Application.status,
            func.count(Application.id)
        )
        .group_by(Application.status)
        .all()
    )

    by_status = {
        status: count
        for status, count in status_counts
    }

    interview_count = by_status.get("Interview", 0)

    conversion_rate = (
        (interview_count / total) * 100
        if total > 0
        else 0
    )

    return {
        "total_applications": total,
        "by_status": by_status,
        "interview_conversion_rate": round(conversion_rate, 2)
    }