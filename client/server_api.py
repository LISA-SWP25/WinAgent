import requests
import logging

BASE_URL = "http://localhost:8000/api"  # или IP адрес сервера LISA

def generate_agent_config(role_id: int, template_id: int):
    url = f"{BASE_URL}/agents/generate"
    payload = {
        "role_id": role_id,
        "template_id": template_id
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Ошибка при генерации конфига агента: {e}")
        return None

def test_generate_agent_config(setup_db):
    payload = {
        "name": "TestAgent",
        "role_id": setup_db["role_id"],
        "template_id": setup_db["template_id"],
        "os_type": "linux",
        "injection_target": "sshd",
        "stealth_level": 5,
        "custom_config": {"delay": 3}
    }

    response = client.post("/agents/generate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "agent_id" in data
    assert data["config"]["name"] == "TestAgent"
    assert data["config"]["target_os"] == "linux"
    assert data["config"]["stealth_level"] == 5
    assert data["download_url"].startswith("/api/agents")

def download_agent_config(agent_id: str):
    url = f"{BASE_URL}/agents/{agent_id}/config/download?format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Ошибка при загрузке конфига агента: {e}")
        return None


def fetch_template(template_id):
    url = f"{BASE_URL}/templates/{template_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Ошибка при получении шаблона поведения: {e}")
        return None

def send_activity(agent_id, action, data=None):
    url = f"{BASE_URL}/agent_activities"
    payload = {
        "agent_id": agent_id,
        "activity_type": action,
        "activity_data": data or {}
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        logging.warning(f"Ошибка при логировании действия: {e}")
