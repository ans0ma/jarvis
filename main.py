import config
from listener import listen
from commands import execute

STOP_WORDS = ("стоп", "выход")


def main():
    config.check_config()
    print("Jarvis запущен. Говорите команды. Для выхода нажмите Ctrl+C или скажите 'стоп'.")

    while True:
        text = listen()
        if not text:
            continue

        if any(word in text for word in STOP_WORDS):
            print("Останавливаюсь.")
            break

        execute(text)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nJarvis остановлен.")