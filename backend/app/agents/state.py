from typing import Any, TypedDict

from app.schemas.case import CaseCreateRequest


class SupportState(TypedDict, total=False):
    request: CaseCreateRequest
    transcript: str
    normalized_message: str
    intent: str
    sentiment: float
    priority: str
    account: dict[str, Any]
    knowledge: list[dict[str, Any]]
    recommendation: str
    confidence: float
    handover_required: bool
    handover_reason: str
    ticket_subject: str
    audit_trail: list[dict[str, Any]]
