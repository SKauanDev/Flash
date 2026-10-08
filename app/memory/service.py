from sqlalchemy.orm import Session

from app.db.repositories import list_memories, recent_messages, set_memory


def build_context(db: Session, user_id: int, message_limit: int = 20) -> dict:
    return {
        "messages": [
            {"role": item.role, "content": item.content}
            for item in recent_messages(db, user_id, message_limit)
        ],
        "memories": [
            {"key": item.key, "value": item.value}
            for item in list_memories(db, user_id)
        ],
    }


def remember(db: Session, user_id: int, key: str, value: str) -> None:
    set_memory(db, user_id, key, value)
