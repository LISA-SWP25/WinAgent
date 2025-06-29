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

mac = uuid.getnode()
mac_str = ':'.join(f'{(mac >> ele) & 0xff:02x}' for ele in range(40, -1, -8))
agent_id = f"agent_{mac:012x}"  

AGENT_ID = "agent_001"

from utils.logger import setup_logger

logger = setup_logger()

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


def weighted_choice(activities):
    weights = [a.get("weight", 1) for a in activities]
    return random.choices(activities, weights=weights, k=1)[0]


def run_action(action, paths):
    action_type = action.get("action")

    if action_type == "open_app":
        app_name = action.get("app")
        path = paths.get("apps", {}).get(app_name)
        if path:
            apps.open_app(path)
        else:
            logging.warning(f"Неизвестное приложение: {app_name}")

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
            logging.warning(f"Неизвестный терминал: {terminal}")

    elif action_type == "edit_file":
        path = os.path.expandvars(action.get("path", ""))
        files.edit_file(path)

    elif action_type == "sleep":
        seconds = action.get("seconds", 60)
        logging.info(f"Пауза на {seconds} секунд")
        time.sleep(seconds)

    elif action_type == "simulate_activity":
        net.simulate_network_activity()

    else:
        logging.error(f"Неизвестное действие: {action_type}")


def is_work_time(settings):
    now = datetime.now()
    weekday = now.isoweekday()
    current_time = now.time()
    work_days = settings["work_days"]
    start = datetime.strptime(settings["work_start"], "%H:%M").time()
    end = datetime.strptime(settings["work_end"], "%H:%M").time()
    return weekday in work_days and start <= current_time <= end


def test_agent_main_workflow():
    with patch('agent.download_agent_config') as mock_download, \
         patch('agent.send_activity') as mock_send, \
         patch('agent.run_action') as mock_run, \
         patch('agent.time.sleep') as mock_sleep, \
         patch('agent.logger') as mock_logger:
        
        # Настраиваем моки
        mock_download.return_value = {
            "custom_config": {
                "interval": 5,
                "randomize": False
            },
            "behavior_template": {
                "tasks": ["test_action"]
            }
        }
        
        mock_sleep.side_effect = KeyboardInterrupt()
        try:
            from agent import main
            main()
        except KeyboardInterrupt:
            pass
        mock_download.assert_called_once_with("agent_001")
        mock_run.assert_called_once()
        mock_send.assert_called_once_with("agent_001", "test_action", {"status": "ok"})
        mock_logger.info.assert_any_call("Аgent: agent_001, Interval: 5, TAsks: ['test_action']")

def main():
    logger.info("Запуск агента LISA с конфигурацией по ID")

    config = download_agent_config(AGENT_ID)
    if not config:
        logger.error("Конфигурация агента не получена. Завершение.")
        return

    interval = config.get("custom_config", {}).get("interval", 10)
    randomize = config.get("custom_config", {}).get("randomize", True)
    tasks = config.get("behavior_template", {}).get("tasks", [])

    if not tasks:
        logger.error("Шаблон задач пуст. Завершение.")
        return

    logger.info(f"Агент: {AGENT_ID}, Интервал: {interval}, Задачи: {tasks}")

    while True:
        task = random.choice(tasks) if randomize else tasks[0]
        action = {"action": task}
        run_action(action, paths={})  # paths можно убрать, если не используется

        send_activity(AGENT_ID, task, {"status": "ok"})
        logger.info(f"Ожидание {interval} секунд")
        time.sleep(interval)


if __name__ == "__main__":
    main()
