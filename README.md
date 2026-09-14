# Jarvis — голосовой ассистент

Лёгкий голосовой ассистент с интерфейсом командной строки (CLI). Слушает голосовые
команды, распознаёт их и выполняет действия: открывает и сворачивает/разворачивает приложения, отправляет
сообщения в Telegram и т.д.

> **Поддерживается только Windows.**


## Требования

- Windows 10/11
- Python 3.13, добавленный в PATH


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

```cmd
git clone https://github.com/ans0ma/jarvis.git
cd jarvis
python3.13 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

> **Если используете PowerShell** и при активации окружения видите ошибку вида
> `... cannot be loaded because running scripts is disabled on this system`, значит
> политика выполнения скриптов блокирует активацию. Разрешите её для текущего
> пользователя:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> и повторите `venv\Scripts\activate`. В обычной `cmd` эта ошибка не возникает.

Скопируйте `.env.example` в `.env` и заполните своими токенами для работы команд, связанных с Telegram.


## Запуск

```cmd
python main.py
```