from sqlalchemy.orm import Session

from app.db.models import AuditEvent


def audit_event(db: Session, event_type: str, payload: dict, actor: str = "system") -> None:
    db.add(AuditEvent(event_type=event_type, actor=actor, payload=payload))
    db.commit()
