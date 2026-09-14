import speech_recognition as sr

recognizer = sr.Recognizer()


def listen():
    """Слушает микрофон один раз и возвращает распознанный текст.
    Если не удалось разобрать — возвращает None."""
    with sr.Microphone() as source:
        print("Слушаю...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="ru-RU").lower()
        print(f"Распознано: {text}")
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as error:
        print(f"Ошибка сервиса распознавания: {error}")
        return None