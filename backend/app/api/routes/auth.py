from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.models import Customer
from app.db.session import get_db
from app.schemas.auth import DemoLoginRequest, TokenResponse

router = APIRouter()


@router.post("/demo-login", response_model=TokenResponse)
def demo_login(payload: DemoLoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    customer = db.scalar(select(Customer).where(Customer.email == payload.email))
    if customer is None:
        raise HTTPException(status_code=404, detail="Demo customer not found")
    token = create_access_token(customer.id, {"email": customer.email, "role": "customer"})
    return TokenResponse(access_token=token, customer_id=customer.id)
