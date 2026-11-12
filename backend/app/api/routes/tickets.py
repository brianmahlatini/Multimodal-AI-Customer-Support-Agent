from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Ticket, TicketStatus
from app.db.session import get_db
from app.schemas.ticket import TicketResponse, TicketUpdateRequest

router = APIRouter()


@router.get("", response_model=list[TicketResponse])
def list_tickets(db: Session = Depends(get_db)) -> list[TicketResponse]:
    tickets = db.scalars(select(Ticket).order_by(Ticket.created_at.desc())).all()
    return [to_response(ticket) for ticket in tickets]


@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: str, payload: TicketUpdateRequest, db: Session = Depends(get_db)) -> TicketResponse:
    ticket = db.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if payload.status:
        ticket.status = TicketStatus(payload.status)
    if payload.owner is not None:
        ticket.owner = payload.owner
    db.commit()
    db.refresh(ticket)
    return to_response(ticket)


def to_response(ticket: Ticket) -> TicketResponse:
    return TicketResponse(
        id=ticket.id,
        case_id=ticket.case_id,
        status=ticket.status.value,
        owner=ticket.owner,
        subject=ticket.subject,
        priority=ticket.priority,
        handover_required=ticket.handover_required,
    )
