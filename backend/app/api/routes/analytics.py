from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.analytics_service import analytics_summary

router = APIRouter()


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)) -> dict:
    return analytics_summary(db)
