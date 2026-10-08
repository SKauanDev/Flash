from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse
from app.config import settings
from app.db.session import SessionLocal
from app.services.messages import process_text_message

router = APIRouter(prefix="/webhooks/whatsapp", tags=["whatsapp"])

@router.get("", response_class=PlainTextResponse)
async def verify(hub_mode: str = Query(alias="hub.mode"), hub_verify_token: str = Query(alias="hub.verify_token"), hub_challenge: str = Query(alias="hub.challenge")) -> str:
    if hub_mode == "subscribe" and hub_verify_token == settings.whatsapp_verify_token:
        return hub_challenge
    raise HTTPException(status_code=403, detail="Invalid verification token")

@router.post("")
async def receive(payload: dict) -> dict:
    processed = 0
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            for message in value.get("messages", []):
                if message.get("type") != "text":
                    continue
                sender = message.get("from")
                body = message.get("text", {}).get("body", "").strip()
                if not sender or not body:
                    continue
                contacts = value.get("contacts", [])
                profile = contacts[0].get("profile", {}) if contacts else {}
                with SessionLocal() as db:
                    result = await process_text_message(db, sender, body, profile.get("name"), message.get("id"))
                if result is not None:
                    processed += 1
    return {"received": True, "processed": processed}
