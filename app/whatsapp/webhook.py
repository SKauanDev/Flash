from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse

from app.config import settings

router = APIRouter(prefix="/webhooks/whatsapp", tags=["whatsapp"])


@router.get("", response_class=PlainTextResponse)
async def verify(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
) -> str:
    if hub_mode == "subscribe" and hub_verify_token == settings.whatsapp_verify_token:
        return hub_challenge
    return "forbidden"


@router.post("")
async def receive(payload: dict) -> dict[str, bool]:
    # Parsing, signature validation and message dispatch will be added next.
    return {"received": True}
