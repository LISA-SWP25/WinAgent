import requests
import time
import webbrowser
import random

# === Настройки ===
BASE_URL = "http://localhost:8000"
AGENT_ID = "agent_001"
CONFIG_URL = f"{BASE_URL}/api/agents/{AGENT_ID}/config/download"

# === Загрузка конфигурации ===
def fetch_agent_config():
    try:
        response = requests.get(CONFIG_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[!] Ошибка загрузки конфигурации: {e}")
        return None

# === Задача: открыть браузер ===
def open_browser(url="https://example.com"):
    print(f"[+] Открываю браузер по адресу: {url}")
    webbrowser.open(url)

# === Задача: симуляция активности ===
def simulate_activity(duration=5):
    print(f"[+] Симулирую активность пользователя на {duration} секунд...")
    for i in range(duration):
        print(f"    ...активность... ({i+1}s)")
        time.sleep(1)

# === Основной цикл ===
def main():
    config = fetch_agent_config()
    if not config:
        return

    tasks = config.get("behavior_template", {}).get("tasks", [])
    interval = config.get("custom_config", {}).get("interval", 5)
    randomize = config.get("custom_config", {}).get("randomize", False)

    print(f"[*] Задачи агента: {tasks}")
    print(f"[*] Интервал: {interval}, случайность: {randomize}")

    while True:
        for task in tasks:
            if task == "open_browser":
                open_browser()
            elif task == "simulate_activity":
                simulate_activity()
            else:
                print(f"[!] Неизвестная задача: {task}")

            wait = interval
            if randomize:
                wait = random.randint(1, interval * 2)

            print(f"[*] Ожидание {wait} секунд...\n")
            time.sleep(wait)

if __name__ == "__main__":
    main()