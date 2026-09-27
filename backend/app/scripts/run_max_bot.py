import time

import httpx

from app.services.max_client import MaxClient


WELCOME_TEXT = (
    "Здравствуйте! 👋\n\n"
    "Я — Маршрут+, помощник для родителей "
    "после получения заключения ПМПК.\n\n"
    "Сервис помогает понять:\n"
    "• что сделать дальше;\n"
    "• какие шаги уже выполнены;\n"
    "• какой шаг следующий;\n"
    "• на какой официальный источник "
    "опирается маршрут.\n\n"
    "Сейчас используется тестовый сценарий "
    "для Хабаровского края."
)


HELP_TEXT = (
    "Маршрут+ работает с родителями, "
    "которые уже получили заключение ПМПК.\n\n"
    "Напишите /start, чтобы начать."
)


def extract_user_id(
    update: dict,
) -> int | None:
    user = update.get("user")

    if isinstance(user, dict):
        user_id = user.get("user_id")

        if user_id is not None:
            return int(user_id)

    message = update.get("message")

    if isinstance(message, dict):
        sender = message.get("sender")

        if isinstance(sender, dict):
            user_id = sender.get("user_id")

            if user_id is not None:
                return int(user_id)

    return None


def extract_text(
    update: dict,
) -> str:
    message = update.get("message")

    if not isinstance(message, dict):
        return ""

    body = message.get("body")

    if not isinstance(body, dict):
        return ""

    text = body.get("text")

    if not isinstance(text, str):
        return ""

    return text.strip()


def process_update(
    client: MaxClient,
    update: dict,
) -> None:
    update_type = update.get(
        "update_type"
    )

    user_id = extract_user_id(
        update
    )

    print(
        f"Update: {update_type}, "
        f"user_id={user_id}"
    )

    if user_id is None:
        return

    if update_type == "bot_started":
        client.send_message(
            user_id=user_id,
            text=WELCOME_TEXT,
        )
        return

    if update_type == "message_created":
        text = extract_text(
            update
        )

        print(
            f"Message text: {text!r}"
        )

        if text.lower() in {
            "/start",
            "start",
            "начать",
        }:
            client.send_message(
                user_id=user_id,
                text=WELCOME_TEXT,
            )
        else:
            client.send_message(
                user_id=user_id,
                text=HELP_TEXT,
            )


def run() -> None:
    client = MaxClient()

    try:
        subscriptions = (
            client.get_subscriptions()
        )

        if subscriptions:
            raise RuntimeError(
                "У бота уже настроен Webhook. "
                "Long Polling одновременно "
                "с Webhook использовать нельзя."
            )

        print(
            "MAX bot polling started."
        )
        print(
            "Press Ctrl+C to stop."
        )

        marker = None

        while True:
            try:
                data = client.get_updates(
                    marker=marker,
                )

                updates = data.get(
                    "updates",
                    [],
                )

                new_marker = data.get(
                    "marker"
                )

                for update in updates:
                    process_update(
                        client,
                        update,
                    )

                if new_marker is not None:
                    marker = new_marker

            except httpx.HTTPError as exc:
                print(
                    f"MAX API error: {exc}"
                )

                time.sleep(3)

    except KeyboardInterrupt:
        print(
            "\nMAX bot polling stopped."
        )

    finally:
        client.close()


if __name__ == "__main__":
    run()