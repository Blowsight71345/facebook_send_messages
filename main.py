import httpx
from pydantic import BaseModel, HttpUrl
from typing import Dict, Any


class TextOrMediaMessage(BaseModel):
    recipient: Dict[str, str]
    messaging_type: str
    message: Dict[str, Any]


class MessengerAPI:
    BASE_URL = "https://graph.facebook.com/v20.0"

    def __init__(self, page_id: str, access_token: str):
        self.page_id = page_id
        self.access_token = access_token
        self.url = f"{self.BASE_URL}/{self.page_id}/messages"

    async def send_text_message(self, psid: str, text: str) -> Dict[str, Any]:
        message_data = TextOrMediaMessage(
            recipient={"id": psid},
            messaging_type="RESPONSE",
            message={"text": text}
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url,
                params={"access_token": self.access_token},
                json=message_data.model_dump()
            )
            response.raise_for_status()
            return response.json()

    async def send_media_message(self, psid: str,
                                 media_url: HttpUrl) -> Dict[str, Any]:
        attachment = {
            "type": "image",
            #Отправляемые сообщения могут содержать контент следующих типов:
            # Аудио
            # Кнопки
            # Файлы
            # Меню
            # GIF-файлы
            # Изображения
            # Шаблоны
            # Текст
            # Видео
            "payload": {
                "url": media_url,
                "is_reusable": True
            }
        }
        message_date = TextOrMediaMessage(
            recipient={"id": psid},
            messaging_type="RESPONSE",
            message={"attachment": attachment}
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url,
                params={"access_token": self.access_token},
                json=message_date.model_dump()
            )
            response.raise_for_status()
            return response.json()
