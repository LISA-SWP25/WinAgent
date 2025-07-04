import os
import logging

def edit_file(path):
    try:
        os.startfile(path)
        logging.info(f"Файл открыт: {path}")
    except Exception as e:
        logging.error(f"Ошибка при открытии файла: {e}")
