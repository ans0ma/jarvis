# Jarvis — голосовой ассистент

Лёгкий голосовой ассистент с интерфейсом командной строки (CLI). Слушает голосовые
команды, распознаёт их и выполняет действия: открывает и сворачивает/разворачивает приложения, отправляет
сообщения в Telegram и т.д. Windows-only.


## Структура проекта

```
jarvis/
├── main.py            # точка входа, главный цикл
├── listener.py        # захват голоса и STT
├── commands.py        # словарь команд
├── actions/
│   ├── apps.py         # открытие приложений
│   └── telegram.py     # отправка сообщений в Telegram
├── config.py           # настройки, загрузка токенов из .env
└── requirements.txt
```


## Установка

### Из стабильной ветки для использования:

```bash
git clone https://github.com/ans0ma/jarvis.git
cd jarvis
python3.13 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Скопируйте `.env.example` в `.env` и заполните своими токенами.

### Из ветки главного разработчика для дальнейшей разработки:

```bash
git clone -b ans0ma --single-branch https://github.com/ans0ma/jarvis.git
cd jarvis
python3.13 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Скопируйте `.env.example` в `.env` и заполните своими токенами.


## Запуск

```bash
python main.py
```