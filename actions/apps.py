import logging
import subprocess


def open_app(path):
    try:
        subprocess.Popen([path], shell=True)
        logging.info(f"The application is running: {path}")
    except Exception as e:
        logging.error(f"Startup error {path}: {e}")


def open_browser(url):
    try:
        subprocess.Popen(["start", "", url], shell=True)
        logging.info(f"The browser opened the URL: {url}")
    except Exception as e:
        logging.error(f"Error when opening the browser: {e}")


def run_terminal_command(term_path, command):
    try:
        subprocess.Popen([term_path, "/c", command], shell=True)
        logging.info(f"The command was executed: {command}")
    except Exception as e:
        logging.error(f"Command error {command}: {e}")


def open_settings():
    try:
        subprocess.Popen(["start", "ms-settings:"], shell=True)
        logging.info("Windows Settings are open")
    except Exception as e:
        logging.error(f"Error when opening settings: {e}")


def open_ad_utilities():
    try:
        subprocess.Popen(["mmc", "dsa.msc"], shell=True)
        logging.info("Открыт Active Directory Users and Computers")
    except Exception as e:
        logging.error(f"Error when opening AD: {e}")
