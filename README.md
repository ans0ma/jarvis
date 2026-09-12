# Jarvis — голосовой ассистент

Лёгкий голосовой ассистент с интерфейсом командной строки (CLI). Слушает голосовые
команды, распознаёт их и выполняет действия: открывает приложения, отправляет
сообщения в Telegram и т.д. Windows-only.


## Структура проекта

```
jarvis/
├── main.py            # точка входа, главный цикл: слушать → распознать → выполнить
├── listener.py        # захват голоса и STT
├── commands.py        # словарь команд: текст → функция-обработчик
├── actions/
│   ├── apps.py         # открытие приложений
│   └── telegram.py     # отправка сообщений в Telegram
├── config.py           # настройки, загрузка токенов из .env
└── requirements.txt
```


## Установка

```bash
git clone <https://github.com/ans0ma/jarvis.git>
cd jarvis
python3.13 -m venv venv
venv\Scripts\activate (Windows)
pip install -r requirements.txt
```

Скопируйте `.env.example` в `.env` и заполните своими токенами.


## Запуск

```bash
python main.py
```