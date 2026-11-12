from pydantic import BaseModel, EmailStr


class DemoLoginRequest(BaseModel):
    email: EmailStr = "alex.rivera@example.com"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    customer_id: str
