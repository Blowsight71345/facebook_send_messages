import pytest
from httpx import Response
from unittest.mock import AsyncMock, patch

from main import MessengerAPI


@pytest.mark.asyncio
async def test_send_text_message():
    access_token = "PAGE-ACCESS-TOKEN"
    page_id = "PAGE-ID"
    client = MessengerAPI(page_id=page_id, access_token=access_token)
    psid = "USER_PSID"
    text = "Hello, world!"

    with patch('httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
        mock_post.return_value = AsyncMock(spec=Response)
        mock_post.return_value.json.return_value = {
            "recipient_id": psid,
            "message_id": "AG5Hz2U..."
        }
        mock_post.return_value.status_code = 200
        response = await client.send_text_message(psid, text)

        assert response["recipient_id"] == psid
        assert response["message_id"] == "AG5Hz2U..."

        mock_post.assert_called_once_with(
            client.url,
            params={"access_token": access_token},
            json={
                "recipient": {"id": psid},
                "messaging_type": "RESPONSE",
                "message": {"text": text}
            },
        )


@pytest.mark.asyncio
async def test_send_media_message():
    access_token = "PAGE-ACCESS-TOKEN"
    page_id = "PAGE-ID"
    client = MessengerAPI(page_id=page_id, access_token=access_token)
    psid = "USER_PSID"
    media_url = "http://www.messenger-rocks.com/image.jpg"

    with patch('httpx.AsyncClient.post', new_callable=AsyncMock) as mock_post:
        mock_post.return_value = AsyncMock(spec=Response)
        mock_post.return_value.json.return_value = {
            "recipient_id": psid,
            "message_id": "AG5Hz2U..."
        }
        mock_post.return_value.status_code = 200
        response = await client.send_media_message(psid, media_url)

        assert response["recipient_id"] == psid
        assert response["message_id"] == "AG5Hz2U..."

        mock_post.assert_called_once_with(
            client.url,
            params={"access_token": access_token},
            json={
                "recipient": {"id": psid},
                "messaging_type": "RESPONSE",
                "message": {
                    "attachment": {
                        "type": "image",
                        "payload": {
                            "url": media_url,
                            "is_reusable": True}
                    }
                }
            },
        )
