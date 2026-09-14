"""
Отправка сообщений в Telegram через Telethon (user-API).

Что тут происходит:
- TelegramClient создаётся один раз (лениво, при первом вызове) и переиспользуется,
  а не создаётся заново на каждое сообщение.
- Авторизация хранится в session-файле (jarvis_session.session). Он появляется
  рядом с этим модулем после первого успешного логина и содержит уже готовый
  ключ доступа — при следующих запусках Telethon логинится по нему автоматически,
  без повторного ввода кода из SMS/Telegram.
- Получатель ("мама", "олег") сопоставляется с реальным username/номером через
  contacts.json — простой JSON-словарь, без базы данных.
- Все ошибки перехватываются внутри этой функции и просто печатаются: ассистент
  не должен падать целиком из-за того, что не отправилось одно сообщение.
"""

import json
import os

# Импортируем из telethon.sync, а не из telethon — это даёт синхронный API.
# Без .sync каждый метод клиента был бы корутиной, которую нужно await'ить,
# а это потребовало бы переписать весь проект на asyncio. С .sync Telethon сам
# поднимает event loop под капотом, и client.send_message(...) можно вызывать
# как обычную синхронную функцию — то, что нужно для MVP в духе остального кода.
from telethon.sync import TelegramClient
from telethon.errors import RPCError

from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE

# Базовое имя session-файла. Telethon сам допишет расширение .session.
# Файл появится в той же папке, откуда запущен main.py (то есть в корне проекта).
SESSION_NAME = "jarvis_session"

CONTACTS_FILE = os.path.join(os.path.dirname(__file__), "..", "contacts.json")

# Ключевые слова, после которых в тексте команды ожидается "<получатель> <сообщение>"
TRIGGER_WORDS = {"напиши", "отправь"}

_client = None  # см. _get_client() — создаём подключение один раз, а не при каждом вызове


def _get_client():
    """Возвращает уже существующий TelegramClient или создаёт новый при первом вызове.
    Само создание TelegramClient(...) ещё не подключается к серверам Telegram —
    подключение происходит позже, в client.start()."""
    global _client
    if _client is None:
        _client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)
    return _client


def _load_contacts():
    """Загружает словарь вида {"мама": "@mama_username"} из contacts.json.
    Файл специально вынесен отдельно от config.py: это не секрет вроде токена,
    а обычные пользовательские данные, которые удобно редактировать руками."""
    if not os.path.exists(CONTACTS_FILE):
        print(
            f"[telegram] Файл контактов не найден: {CONTACTS_FILE}. "
            "Создайте contacts.json по примеру contacts.example.json."
        )
        return {}
    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"[telegram] contacts.json повреждён (ошибка JSON): {e}")
        return {}


def _parse_recipient_and_message(text):
    """Достаёт получателя и текст сообщения из фразы вида
    'напиши маме привет опаздываю' -> ('маме', 'привет опаздываю').

    Правило нарочно простое (это MVP, сложный разбор фраз — будущий этап
    из PLAN.md): берём первое слово после триггера как получателя,
    всё что после него — как текст сообщения."""
    words = text.split()

    trigger_index = None
    for i, word in enumerate(words):
        if word in TRIGGER_WORDS:
            trigger_index = i
            break

    if trigger_index is None:
        return None, None

    remaining = words[trigger_index + 1:]
    if len(remaining) < 2:
        # Нет отдельно получателя и текста ("напиши маме" без самого сообщения)
        return None, None

    recipient_key = remaining[0]
    message = " ".join(remaining[1:])
    return recipient_key, message


def send_telegram_message(text):
    """Точка входа, которую вызывает commands.py вместо старой заглушки.
    Разбирает фразу, ищет получателя в contacts.json и отправляет сообщение.
    Ничего не бросает наружу — все проблемы печатаются в консоль, чтобы
    голосовой ассистент не падал целиком из-за одной неудачной отправки."""

    recipient_key, message = _parse_recipient_and_message(text)
    if not recipient_key or not message:
        print(f"[telegram] Не удалось понять, кому и что написать: «{text}»")
        return

    contacts = _load_contacts()
    target = contacts.get(recipient_key)
    if not target:
        print(
            f"[telegram] Получатель «{recipient_key}» не найден в contacts.json. "
            f"Известные получатели: {', '.join(contacts.keys()) or 'нет ни одного'}."
        )
        return

    if not TELEGRAM_API_ID or not TELEGRAM_API_HASH:
        print("[telegram] Не заданы TELEGRAM_API_ID/TELEGRAM_API_HASH в .env — отправка невозможна.")
        return

    client = _get_client()
    try:
        # client.start() подключается и логинится. Если session-файл уже есть
        # и авторизация в нём валидна — это происходит мгновенно и молча.
        # Если файла нет (самый первый запуск) — Telethon сам спросит в консоли
        # код подтверждения, который придёт в Telegram/SMS на TELEGRAM_PHONE.
        client.start(phone=TELEGRAM_PHONE)
        client.send_message(target, message)
        print(f"[telegram] Сообщение отправлено «{recipient_key}»: {message}")
    except RPCError as e:
        # Ошибки на стороне Telegram: неверный username, флуд-контроль и т.п.
        print(f"[telegram] Telegram отклонил запрос: {e}")
    except (ConnectionError, OSError) as e:
        # Проблемы с сетью/подключением
        print(f"[telegram] Нет соединения с Telegram: {e}")
    except Exception as e:
        # Подстраховка: любая другая ошибка не должна ронять весь ассистент
        print(f"[telegram] Непредвиденная ошибка при отправке: {e}")
