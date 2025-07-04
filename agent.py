import getpass
import logging
import os
import random
import time
import uuid
from datetime import datetime
from pathlib import Path

import yaml

from actions import apps, files, net
from client.server_api import send_activity, download_agent_config
from utils.logger import setup_logger

# === Генерация уникального AGENT_ID ===

username = getpass.getuser()
mac_int = uuid.getnode()
mac_str = f"{mac_int:012x}"
AGENT_ID = f"agent_{username}_{mac_str}".lower()

# === Инициализация логгера ===
logger = setup_logger()

# === Singleton: файл-блокировка ===

LOCK_FILE = Path(f"{AGENT_ID}.lock")


def check_singleton():
    if LOCK_FILE.exists():
        logger.error(f"The agent with the ID {AGENT_ID} has already been launched! Completion.")
        sys.exit(1)
    else:
        LOCK_FILE.touch()
        logger.info(f"A blocking file has been created {LOCK_FILE}")


def cleanup_singleton():
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
        logger.info(f"The lock file {LOCK_FILE} has been deleted")


# === Пути к локальным конфигам (если используются) ===

CONFIG_PATH = Path("config/settings.yaml")
PATHS_PATH = Path("config/paths.yaml")
ROLES_DIR = Path("roles")


def load_yaml(path):
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_config():
    settings = load_yaml(CONFIG_PATH)
    paths = load_yaml(PATHS_PATH)
    role_name = settings["role"]
    role_file = ROLES_DIR / f"{role_name}.yaml"
    role = load_yaml(role_file)
    return settings, paths, role


# === Выбор случайной активности по весам ===

def weighted_choice(activities):
    weights = [a.get("weight", 1) for a in activities]
    return random.choices(activities, weights=weights, k=1)[0]


# === Основной исполнитель действий ===

import sys


def run_action(action, paths):
    action_type = action.get("action")

    # Задержка перед выполнением, если указана
    delay = action.get("delay")
    if delay:
        logging.info(f"Delay of {delay} seconds before the action {action_type}")
        time.sleep(delay)

    if action_type == "open_app":
        app_name = action.get("app")
        path = paths.get("apps", {}).get(app_name)

        if path == "ms-settings:":
            apps.open_settings()
        elif "dsa.msc" in path:
            apps.open_ad_utilities()
        elif path:
            apps.open_app(path)
        else:
            logging.warning(f"Unknown application: {app_name}")

    elif action_type == "open_browser":
        urls = action.get("urls", ["https://example.com"])
        url = random.choice(urls)
        apps.open_browser(url)

    elif action_type == "run_terminal_command":
        terminal = action.get("terminal")
        command = action.get("command")
        term_path = paths.get("apps", {}).get(terminal)
        if term_path:
            apps.run_terminal_command(term_path, command)
        else:
            logging.warning(f"Unknown terminal: {terminal}")

    elif action_type == "edit_file":
        path = os.path.expandvars(action.get("path", ""))
        files.edit_file(path)

    elif action_type == "sleep":
        seconds = action.get("seconds", 60)
        logging.info(f"Pause (sleep) for {seconds} seconds")
        time.sleep(seconds)

    elif action_type == "simulate_activity":
        net.simulate_network_activity()

    elif action_type == "terminate":
        logging.info("The agent is being terminated according to the script.")
        sys.exit(0)

    elif action_type == "os_settings":
        apps.open_settings()

    elif action_type == "ad_utilities":
        apps.open_ad_utilities()


    elif action_type == "conditional_exit":
        condition = action.get("condition")
        # Пример: проверка нерабочего времени
        if condition == "not_work_time" and not is_work_time({}):  # передай settings если нужно
            logging.info("The condition is met: the agent is shutting down.")
            sys.exit(0)
        else:
            logging.info("The completion condition is not met — the agent continues to work.")

    else:
        logging.error(f"Unknown action: {action_type}")


# === Проверка рабочего времени ===

def is_work_time(settings):
    now = datetime.now()
    weekday = now.isoweekday()
    current_time = now.time()
    work_days = settings["work_days"]
    start = datetime.strptime(settings["work_start"], "%H:%M").time()
    end = datetime.strptime(settings["work_end"], "%H:%M").time()
    return weekday in work_days and start <= current_time <= end


# === Основной цикл ===

def main():
    check_singleton()
    logger.info("Launching the LISA agent with the configuration by ID")

    try:
        config = download_agent_config(AGENT_ID)
        if not config:
            logger.error("The agent configuration was not received. Completion.")
            return

        interval = config.get("custom_config", {}).get("interval", 10)
        randomize = config.get("custom_config", {}).get("randomize", True)
        tasks = config.get("behavior_template", {}).get("tasks", [])

        if not tasks:
            logger.error("The task template is empty. Completion.")
            return

        logger.info(f"Agent: {AGENT_ID}, Interval: {interval}, Tasks: {tasks}")
        settings, paths, _ = load_config()

        if randomize:
            while True:
                task = weighted_choice(tasks)
                run_action(task, paths=paths)

                send_activity(AGENT_ID, task, {"status": "ok"})
                logger.info(f"Waiting {interval} seconds")
                time.sleep(interval)
        else:
            while True:
                for task in tasks:
                    run_action(task, paths=paths)

                    send_activity(AGENT_ID, task, {"status": "ok"})
                    logger.info(f"Waiting {interval} seconds")
                    time.sleep(interval)

    finally:
        cleanup_singleton()


# === Запуск ===

if __name__ == "__main__":
    main()
