from actions.apps import open_app, minimize_all, restore_all
from actions.telegram import send_telegram_message


def execute(text):
    """Принимает распознанный текст, находит все подходящие команды
    в фразе и выполняет каждую по очереди."""
    matched = False

    if "отошел" in text or "отошёл" in text:
        minimize_all()
        matched = True

    if "пришел" in text or "пришёл" in text:
        restore_all()
        matched = True

    if "открой" in text:
        open_app(text)
        matched = True

    if "напиши" in text or "отправь" in text:
        send_telegram_message(text)
        matched = True

    if not matched:
        print(f"Команда не распознана: {text}")
