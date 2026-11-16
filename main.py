import config
from commands import execute
from listener import listen

STOP_WORDS = ("стоп", "выход")


def main():
    config.check_config()
    print(
        "Jarvis запущен. Говорите команды. Для выхода нажмите Ctrl+C или скажите 'стоп'."
    )

    while True:
        text = listen()
        if not text:
            continue

        text_lower = text.lower().strip()

        if any(word in text_lower for word in STOP_WORDS):
            print("Останавливаюсь.")
            break

        execute(text_lower)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nJarvis остановлен.")
