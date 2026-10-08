from sqlalchemy.orm import Session
from app.agent.context import make_agent_context
from app.agent.runtime import runtime
from app.db.repositories import add_message, get_or_create_user

async def process_text_message(db: Session, whatsapp_id: str, text: str, display_name: str | None = None, external_id: str | None = None) -> str | None:
    user = get_or_create_user(db, whatsapp_id, display_name)
    existing = add_message(db, user.id, "user", text, external_id)
    if external_id and existing.external_id != external_id:
        return None
    context = make_agent_context(db, user.id, text)
    response = await runtime.handle(db, user.id, context["incoming_message"])
    add_message(db, user.id, "assistant", response.text)
    return response.text
