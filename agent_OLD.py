import requests
import threading
import time
import webbrowser
import random
import tkinter as tk
from tkinter import ttk, messagebox

BASE_URL = "http://localhost:8000"

# === API ===
def fetch_agent_list():
    try:
        res = requests.get(f"{BASE_URL}/api/agents")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch agent list:\n{e}")
        return []

def fetch_agent_config(agent_id):
    try:
        res = requests.get(f"{BASE_URL}/api/agents/{agent_id}/config/download")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch agent config:\n{e}")
        return None

# === Task implementations ===
def open_browser(url="https://example.com"):
    print(f"[+] Opening browser: {url}")
    webbrowser.open(url)

def simulate_activity(duration=5):
    print(f"[+] Simulating user activity for {duration} seconds...")
    for i in range(duration):
        print(f"    ...activity... ({i+1}s)")
        time.sleep(1)

def start_explorer():
    print("[+] Launching File Explorer")
    import subprocess
    subprocess.Popen("explorer")

def start_calc():
    print("[+] Launching Calculator")
    import subprocess
    subprocess.Popen("calc")

# Mapping task names to functions
TASK_MAP = {
    "open_browser": open_browser,
    "simulate_activity": simulate_activity,
    "start_explorer": start_explorer,
    "start_calc": start_calc,
}

# === Run agent tasks ===
def run_tasks(agent_config):
    tasks = agent_config.get("behavior_template", {}).get("tasks", [])
    interval = agent_config.get("custom_config", {}).get("interval", 5)
    randomize = agent_config.get("custom_config", {}).get("randomize", False)

    for task in tasks:
        func = TASK_MAP.get(task)
        if func:
            func()
        else:
            print(f"[!] Unknown task: {task}")

        wait = random.randint(1, interval * 2) if randomize else interval
        print(f"[*] Waiting {wait} seconds...\n")
        time.sleep(wait)

# === GUI ===
class AgentGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agent Runner")
        self.geometry("400x300")
        self.agent_list = []
        self.current_config = None

        self.create_widgets()
        self.load_agents()

    def create_widgets(self):
        ttk.Label(self, text="Select an agent:").pack(pady=5)

        self.agent_combo = ttk.Combobox(self, state="readonly")
        self.agent_combo.pack(fill="x", padx=20)
        self.agent_combo.bind("<<ComboboxSelected>>", self.on_agent_selected)

        ttk.Label(self, text="Tasks:").pack(pady=5)
        self.task_listbox = tk.Listbox(self, height=8)
        self.task_listbox.pack(fill="both", expand=True, padx=20)

        self.run_button = ttk.Button(self, text="Run Tasks", command=self.on_run_clicked)
        self.run_button.pack(pady=10)

    def load_agents(self):
        self.agent_list = fetch_agent_list()
        items = [agent["agent_id"] for agent in self.agent_list]
        self.agent_combo["values"] = items
        if items:
            self.agent_combo.current(0)
            self.on_agent_selected()

    def on_agent_selected(self, event=None):
        agent_id = self.agent_combo.get()
        self.current_config = fetch_agent_config(agent_id)
        self.update_task_list()

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        if not self.current_config:
            return
        tasks = self.current_config.get("behavior_template", {}).get("tasks", [])
        for task in tasks:
            self.task_listbox.insert(tk.END, task)

    def on_run_clicked(self):
        if not self.current_config:
            messagebox.showwarning("Missing configuration", "Please select an agent first.")
            return
        threading.Thread(target=run_tasks, args=(self.current_config,), daemon=True).start()

# === Run application ===
if __name__ == "__main__":
    app = AgentGUI()
    app.mainloop()
