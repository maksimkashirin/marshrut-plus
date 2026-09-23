import httpx

from app.config import settings


def check_max_bot() -> None:
    if not settings.max_bot_token:
        raise RuntimeError(
            "MAX_BOT_TOKEN is not configured"
        )

    response = httpx.get(
        f"{settings.max_api_url}/me",
        headers={
            "Authorization": settings.max_bot_token,
        },
        timeout=15.0,
    )

    response.raise_for_status()

    bot = response.json()

    print("MAX API connection successful")
    print(
        f"Bot ID: {bot.get('user_id')}"
    )
    print(
        f"Name: {bot.get('first_name')}"
    )
    print(
        f"Username: {bot.get('username')}"
    )
    print(
        f"Is bot: {bot.get('is_bot')}"
    )


if __name__ == "__main__":
    check_max_bot()