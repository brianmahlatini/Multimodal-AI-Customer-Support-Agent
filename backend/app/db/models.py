from datetime import datetime
from enum import Enum
from uuid import uuid4

from sqlalchemy import DateTime, Enum as SqlEnum, Float, ForeignKey, JSON, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class CaseStatus(str, Enum):
    open = "open"
    resolved = "resolved"
    escalated = "escalated"


class TicketStatus(str, Enum):
    open = "open"
    pending_human = "pending_human"
    resolved = "resolved"


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    plan: Mapped[str] = mapped_column(String(64))
    account_status: Mapped[str] = mapped_column(String(64), default="active")
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)


class SupportCase(Base):
    __tablename__ = "support_cases"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    customer_id: Mapped[str] = mapped_column(String(64), ForeignKey("customers.id"), index=True)
    channel: Mapped[str] = mapped_column(String(32))
    status: Mapped[CaseStatus] = mapped_column(SqlEnum(CaseStatus), default=CaseStatus.open)
    intent: Mapped[str] = mapped_column(String(64))
    sentiment: Mapped[float] = mapped_column(Float)
    priority: Mapped[str] = mapped_column(String(32))
    summary: Mapped[str] = mapped_column(Text)
    recommended_resolution: Mapped[str] = mapped_column(Text)
    payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer: Mapped[Customer] = relationship()


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    case_id: Mapped[str] = mapped_column(String(36), ForeignKey("support_cases.id"), index=True)
    status: Mapped[TicketStatus] = mapped_column(SqlEnum(TicketStatus), default=TicketStatus.open)
    owner: Mapped[str | None] = mapped_column(String(255), nullable=True)
    subject: Mapped[str] = mapped_column(String(255))
    priority: Mapped[str] = mapped_column(String(32))
    handover_required: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    event_type: Mapped[str] = mapped_column(String(128), index=True)
    actor: Mapped[str] = mapped_column(String(255), default="system")
    payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
