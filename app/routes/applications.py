from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_user_id
from app.models import Application
from app.schemas import ApplicationCreate, ApplicationResponse


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


# CREATE APPLICATION
@router.post("/", response_model=ApplicationResponse)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    new_application = Application(
        **application.model_dump(),
        user_id=current_user_id
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


# GET ALL ACTIVE APPLICATIONS
@router.get("/", response_model=list[ApplicationResponse])
def get_applications(
    status: str | None = None,
    sort: str = "desc",
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    query = db.query(Application).filter(
        Application.user_id == current_user_id,
        Application.is_archived == False
    )

    # Filter by status
    if status:
        query = query.filter(Application.status == status)

    # Sort by application date
    if sort == "asc":
        query = query.order_by(Application.application_date.asc())
    else:
        query = query.order_by(Application.application_date.desc())

    return query.all()


# GET ONE APPLICATION
@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user_id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application


# UPDATE APPLICATION
@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    application_data: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user_id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    for field, value in application_data.model_dump().items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)

    return application


# ARCHIVE APPLICATION
@router.patch("/{application_id}/archive")
def archive_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user_id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    application.is_archived = True

    db.commit()

    return {
        "message": "Application archived successfully"
    }


# DELETE APPLICATION PERMANENTLY
@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user_id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    db.delete(application)
    db.commit()

    return {
        "message": "Application permanently deleted"
    }