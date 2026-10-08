from sqlalchemy.orm import Session

from app.memory.service import build_context


def make_agent_context(db: Session, user_id: int, incoming_message: str) -> dict:
    return {
        "user_id": user_id,
        "incoming_message": incoming_message,
        **build_context(db, user_id),
    }
