from pydantic import BaseModel, Field


class AttachmentInput(BaseModel):
    filename: str
    content_type: str
    storage_url: str | None = None
    extracted_text: str | None = None


class CaseCreateRequest(BaseModel):
    customer_id: str = Field(..., examples=["cus_1001"])
    channel: str = Field(default="chat", examples=["chat"])
    message: str = Field(..., examples=["I was charged twice and need help today."])
    attachments: list[AttachmentInput] = Field(default_factory=list)


class CaseResponse(BaseModel):
    id: str
    customer_id: str
    channel: str
    status: str
    intent: str
    sentiment: float
    priority: str
    summary: str
    recommended_resolution: str
    payload: dict
