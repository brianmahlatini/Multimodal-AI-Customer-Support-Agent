from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import SupportCase, Ticket


def analytics_summary(db: Session) -> dict:
    total_cases = db.scalar(select(func.count(SupportCase.id))) or 0
    escalated = db.scalar(select(func.count(SupportCase.id)).where(SupportCase.status == "escalated")) or 0
    open_tickets = db.scalar(select(func.count(Ticket.id)).where(Ticket.status != "resolved")) or 0
    avg_sentiment = db.scalar(select(func.avg(SupportCase.sentiment))) or 0
    return {
        "total_cases": total_cases,
        "escalated_cases": escalated,
        "open_tickets": open_tickets,
        "average_sentiment": round(float(avg_sentiment), 2),
        "escalation_rate": round(escalated / total_cases, 2) if total_cases else 0,
    }
