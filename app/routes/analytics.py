from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_user_id
from app.models import Application


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/")
def get_analytics(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # Only applications belonging to the logged-in user
    # Archived applications are intentionally included
    # because analytics should preserve application history.
    user_applications = Application.user_id == current_user_id

    # Total applications
    total = (
        db.query(func.count(Application.id))
        .filter(user_applications)
        .scalar()
    )

    # Applications grouped by status
    status_counts = (
        db.query(
            Application.status,
            func.count(Application.id)
        )
        .filter(user_applications)
        .group_by(Application.status)
        .all()
    )

    by_status = {
        status: count
        for status, count in status_counts
    }

    # Applications grouped by company
    company_counts = (
        db.query(
            Application.company,
            func.count(Application.id)
        )
        .filter(user_applications)
        .group_by(Application.company)
        .all()
    )

    by_company = {
        company: count
        for company, count in company_counts
    }

    # Interview conversion rate
    interview_count = by_status.get("Interview", 0)

    conversion_rate = (
        (interview_count / total) * 100
        if total > 0
        else 0
    )

    return {
        "total_applications": total,
        "by_status": by_status,
        "by_company": by_company,
        "interview_conversion_rate": round(conversion_rate, 2)
    }