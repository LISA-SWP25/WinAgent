Getting a list of agents from the server, simulating agent activity, and opening applications
Patterns of behavior:
├── roles/
│   ├── user.yaml             # Шаблон поведения "офисного сотрудника"
│   ├── dev.yaml              # Шаблон поведения "разработчика"
│   └── admin.yaml

├── actions/
│   ├── apps.py               # Launching applications
│   ├── files.py              #  Working with files
│   ├── net.py                # Simulation of network activity
│   └── gui.py                #  GUI automation (pywinauto/pyautogui)
