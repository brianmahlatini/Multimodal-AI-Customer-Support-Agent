from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agents.graph import run_support_graph
from app.db.models import CaseStatus, SupportCase
from app.db.session import get_db
from app.schemas.case import CaseCreateRequest, CaseResponse
from app.services.audit_service import audit_event
from app.services.ticket_service import TicketService

router = APIRouter()


@router.post("", response_model=CaseResponse, status_code=201)
def create_case(payload: CaseCreateRequest, db: Session = Depends(get_db)) -> CaseResponse:
    result = run_support_graph(payload)
    status = CaseStatus.escalated if result["handover_required"] else CaseStatus.open
    support_case = SupportCase(
        customer_id=payload.customer_id,
        channel=payload.channel,
        status=status,
        intent=result["intent"],
        sentiment=result["sentiment"],
        priority=result["priority"],
        summary=result["normalized_message"][:500],
        recommended_resolution=result["recommendation"],
        payload=dict(result),
    )
    db.add(support_case)
    db.commit()
    db.refresh(support_case)

    ticket = TicketService().create_ticket(
        db,
        case_id=support_case.id,
        subject=result["ticket_subject"],
        priority=result["priority"],
        handover_required=result["handover_required"],
    )
    audit_event(db, "case.created", {"case_id": support_case.id, "ticket_id": ticket.id})
    return to_response(support_case)


@router.get("", response_model=list[CaseResponse])
def list_cases(db: Session = Depends(get_db)) -> list[CaseResponse]:
    rows = db.scalars(select(SupportCase).order_by(SupportCase.created_at.desc())).all()
    return [to_response(row) for row in rows]


@router.get("/{case_id}", response_model=CaseResponse)
def get_case(case_id: str, db: Session = Depends(get_db)) -> CaseResponse:
    support_case = db.get(SupportCase, case_id)
    if support_case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return to_response(support_case)


def to_response(support_case: SupportCase) -> CaseResponse:
    return CaseResponse(
        id=support_case.id,
        customer_id=support_case.customer_id,
        channel=support_case.channel,
        status=support_case.status.value,
        intent=support_case.intent,
        sentiment=support_case.sentiment,
        priority=support_case.priority,
        summary=support_case.summary,
        recommended_resolution=support_case.recommended_resolution,
        payload=support_case.payload,
    )
