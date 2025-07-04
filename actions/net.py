import logging
import random

import requests


def simulate_network_activity():
    urls = ["https://example.com", "https://github.com", "https://www.python.org"]
    url = random.choice(urls)
    try:
        response = requests.get(url, timeout=5)
        logging.info(f"Network request: {url} → {response.status_code}")
    except Exception as e:
        logging.warning(f"Error when requesting to {url}: {e}")
