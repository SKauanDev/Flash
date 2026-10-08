from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import Memory, Message, User

def get_or_create_user(db: Session, whatsapp_id: str, display_name: str | None = None) -> User:
    user = db.scalar(select(User).where(User.whatsapp_id == whatsapp_id))
    if user:
        if display_name and user.display_name != display_name:
            user.display_name = display_name
            db.commit()
        return user
    user = User(whatsapp_id=whatsapp_id, display_name=display_name)
    db.add(user); db.commit(); db.refresh(user)
    return user

def add_message(db: Session, user_id: int, role: str, content: str, external_id: str | None = None) -> Message:
    if external_id:
        existing = db.scalar(select(Message).where(Message.external_id == external_id))
        if existing:
            return existing
    message = Message(user_id=user_id, role=role, content=content, external_id=external_id)
    db.add(message); db.commit(); db.refresh(message)
    return message

def recent_messages(db: Session, user_id: int, limit: int = 20) -> list[Message]:
    rows = db.scalars(select(Message).where(Message.user_id == user_id).order_by(Message.created_at.desc()).limit(limit)).all()
    return list(reversed(rows))

def set_memory(db: Session, user_id: int, key: str, value: str) -> Memory:
    memory = db.scalar(select(Memory).where(Memory.user_id == user_id, Memory.key == key))
    if memory:
        memory.value = value
    else:
        memory = Memory(user_id=user_id, key=key, value=value); db.add(memory)
    db.commit(); db.refresh(memory); return memory

def list_memories(db: Session, user_id: int) -> list[Memory]:
    return list(db.scalars(select(Memory).where(Memory.user_id == user_id)).all())
