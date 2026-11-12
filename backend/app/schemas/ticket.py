from pydantic import BaseModel


class TicketResponse(BaseModel):
    id: str
    case_id: str
    status: str
    owner: str | None
    subject: str
    priority: str
    handover_required: bool


class TicketUpdateRequest(BaseModel):
    status: str | None = None
    owner: str | None = None
