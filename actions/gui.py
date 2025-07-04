import logging

import pyautogui


def simulate_typing(text="Hello from agent!"):
    try:
        pyautogui.write(text, interval=0.1)
        logging.info("Text input was performed via pyautogui")
    except Exception as e:
        logging.error(f"GUI stimulation failed: {e}")
