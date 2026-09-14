import subprocess
import pygetwindow as gw

_minimized_by_us = []

APPS = {
    "блокнот": "notepad",
    "калькулятор": "calc",
}

BROWSER_KEYWORD = "браузер"
BROWSER_COMMAND = "start chrome"
BROWSER_WINDOW_TITLE = "Chrome"


def open_app(text):
    if BROWSER_KEYWORD in text:
        open_browser()
        return

    for keyword, command in APPS.items():
        if keyword in text:
            print(f"Открываю: {keyword}")
            subprocess.Popen(command, shell=True)
            return

    print(f"Данных приложений нет в моем словаре: {text}")


def open_browser():
    """Если окно Chrome уже открыто, то переключается на него.
    Если нет — запускает Chrome."""
    windows = gw.getWindowsWithTitle(BROWSER_WINDOW_TITLE)
    if windows:
        print("Chrome уже открыт, переключаюсь на окно")
        window = windows[0]
        if window.isMinimized:
            window.restore()
        window.activate()
    else:
        print("Открываю Chrome")
        subprocess.Popen(BROWSER_COMMAND, shell=True)


def minimize_all():
    """Сворачивает все окна, которые сейчас не свёрнуты,
    и запоминает их, чтобы потом развернуть именно их."""
    global _minimized_by_us
    _minimized_by_us = []

    for window in gw.getAllWindows():
        if not window.isMinimized and window.title.strip():
            window.minimize()
            _minimized_by_us.append(window.title)

    print(f"Свернул окон: {len(_minimized_by_us)}")


def restore_all():
    """Разворачивает только те окна, которые были свёрнуты
    последним вызовом minimize_all()."""
    global _minimized_by_us

    for title in _minimized_by_us:
        windows = gw.getWindowsWithTitle(title)
        if windows:
            windows[0].restore()

    print(f"Развернул окон: {len(_minimized_by_us)}")
    _minimized_by_us = []