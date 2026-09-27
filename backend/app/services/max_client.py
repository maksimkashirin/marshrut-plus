import httpx

from app.config import settings


class MaxClient:
    def __init__(self) -> None:
        if not settings.max_bot_token:
            raise RuntimeError(
                "MAX_BOT_TOKEN is not configured"
            )

        self.client = httpx.Client(
            base_url=settings.max_api_url,
            headers={
                "Authorization": settings.max_bot_token,
            },
            timeout=httpx.Timeout(
                100.0,
                connect=15.0,
            ),
        )

    def get_subscriptions(self) -> list:
        response = self.client.get(
            "/subscriptions",
        )
        response.raise_for_status()

        data = response.json()

        # MAX может вернуть либо массив,
        # либо объект с массивом subscriptions.
        if isinstance(data, list):
            return data

        return data.get(
            "subscriptions",
            [],
        )

    def get_updates(
        self,
        marker: int | None = None,
    ) -> dict:
        params = {
            "timeout": 30,
            "limit": 100,
            "types": (
                "bot_started,"
                "message_created"
            ),
        }

        if marker is not None:
            params["marker"] = marker

        response = self.client.get(
            "/updates",
            params=params,
        )

        response.raise_for_status()

        return response.json()

    def send_message(
        self,
        user_id: int,
        text: str,
    ) -> None:
        body: dict = {
            "text": text,
        }

        if settings.mini_app_url:
            body["attachments"] = [
                {
                    "type": "inline_keyboard",
                    "payload": {
                        "buttons": [
                            [
                                {
                                    "type": "link",
                                    "text": "Открыть Маршрут+",
                                    "url": settings.mini_app_url,
                                }
                            ]
                        ]
                    },
                }
            ]

        response = self.client.post(
            "/messages",
            params={
                "user_id": user_id,
            },
            json=body,
        )

        response.raise_for_status()

    def close(self) -> None:
        self.client.close()