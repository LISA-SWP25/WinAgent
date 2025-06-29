import subprocess
import logging

def open_app(path):
    try:
        subprocess.Popen([path], shell=True)
        logging.info(f"Приложение запущено: {path}")
    except Exception as e:
        logging.error(f"Ошибка при запуске {path}: {e}")

def open_browser(url):
    try:
        subprocess.Popen(["start", "", url], shell=True)
        logging.info(f"Браузер открыл URL: {url}")
    except Exception as e:
        logging.error(f"Ошибка при открытии браузера: {e}")

def run_terminal_command(term_path, command):
    try:
        subprocess.Popen([term_path, "/c", command], shell=True)
        logging.info(f"Выполнена команда: {command}")
    except Exception as e:
        logging.error(f"Ошибка команды {command}: {e}")
