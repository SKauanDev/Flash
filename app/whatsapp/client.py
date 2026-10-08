import httpx
from app.config import settings

class WhatsAppClient:
    base_url = "https://graph.facebook.com/v21.0"
    async def send_text(self, recipient: str, text: str) -> dict:
        if not settings.whatsapp_access_token or not settings.whatsapp_phone_number_id:
            raise RuntimeError("WhatsApp credentials are not configured")
        url = f"{self.base_url}/{settings.whatsapp_phone_number_id}/messages"
        payload = {"messaging_product":"whatsapp","to":recipient,"type":"text","text":{"body":text}}
        headers = {"Authorization": f"Bearer {settings.whatsapp_access_token}"}
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()

whatsapp_client = WhatsAppClient()
