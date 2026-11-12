from sqlalchemy.orm import Session

from app.db.models import Ticket, TicketStatus


class TicketService:
    def create_ticket(
        self,
        db: Session,
        case_id: str,
        subject: str,
        priority: str,
        handover_required: bool,
    ) -> Ticket:
        ticket = Ticket(
            case_id=case_id,
            subject=subject,
            priority=priority,
            handover_required=handover_required,
            status=TicketStatus.pending_human if handover_required else TicketStatus.open,
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket
