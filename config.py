import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_ID_RAW = os.getenv("TELEGRAM_API_ID")
# Telethon требует api_id как int, а os.getenv всегда возвращает строку (или None).
TELEGRAM_API_ID = int(TELEGRAM_API_ID_RAW) if TELEGRAM_API_ID_RAW else None
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")

REQUIRED_VARS = {
    "TELEGRAM_API_ID": TELEGRAM_API_ID,
    "TELEGRAM_API_HASH": TELEGRAM_API_HASH,
    "TELEGRAM_PHONE": TELEGRAM_PHONE,
}


def check_config():
    """Проверка на то, что все обязательные переменные заданы.
    Если чего-то не хватает то выводит предупреждение, но не останавливает программу.
    Вызывается один раз при старте приложения."""
    missing = [name for name, value in REQUIRED_VARS.items() if not value]
    if missing:
        print(
            f"В .env не хватает переменных: {', '.join(missing)}. "
            "Команды, связанные с Telegram, работать не будут. "
            "Скопируйте .env.example в .env и заполните значения."
        )
