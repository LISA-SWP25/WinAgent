import pyautogui
import logging

def simulate_typing(text="Hello from agent!"):
    try:
        pyautogui.write(text, interval=0.1)
        logging.info("Выполнен ввод текста через pyautogui")
    except Exception as e:
        logging.error(f"GUI-симуляция не удалась: {e}")
