import json
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.db.models import Base, Customer

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    seed_customers()


def seed_customers() -> None:
    data_path = Path(__file__).resolve().parents[1] / "data" / "demo_customers.json"
    if not data_path.exists():
        return
    with SessionLocal() as db:
        if db.scalar(select(Customer).limit(1)):
            return
        customers = json.loads(data_path.read_text(encoding="utf-8"))
        for item in customers:
            db.add(Customer(**item))
        db.commit()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
