The general structure of WinAgent  
WinAgent/  
├── actions/ # Logic of actions: launching applications, browser, terminals, etc.  
├── agent.py # Main executable agent: loop, scheduler, server integration  
├── agent.spec # PyInstaller build configuration for creating .exe  
├── agent_OLD.py # The agent's old backup, can be deleted or archived  
├── build/ # PyInstaller build directory (auto-generated)  
├── client/ # Working with the LISA server: API requests (config, status, logs)  
├── config/ # Local YAML configs: settings.yaml, paths.yaml, etc.   
├── dist/ # Final exe (PyInstaller puts it here)
├── logs/ # Agent logs (agent.log)  
├── planner/ # Scheduler (if there is an extension of the script logic)  
├── roles/ # YAML templates for offline behavior (if the server is not used)  
├── run-lisa.ps1 # PowerShell script for launching or testing the agent manually  
├── utils/ # Logger and auxiliary utilities: singleton lock and setup_logger  
├── .venv/ # Python virtual environment  
├── .git/, .idea/ # Git and IDE configs (PyCharm)

agent.py  
• The agent's entry point.   
• Generates the AGENT_ID (by user + mac).  
• Downloads the configuration from the server (download_agent_config).  
• Schedules the cycle: randomize or in order.  
• Calls run_action() to run commands.  
• * Blocks activity and sends logs to the server.

actions/  
• * apps.py : Runs applications (open_api), browsers (open_browser), PowerShell, etc.  
• Other files may be files.py (working with files) and net.py (emulation of network activity).

client/
• server_api.py : REST API requests to the LISA server.  
• Configuration generation (generate_agent_config).  
• Download the config (download_agent_config).  
• Sending activity logs (send_activity)

config/  
• settings.yaml: General agent settings (role, schedule, interval).  
• paths.yaml: Paths to Windows applications (Word, Excel, Docker, AD, etc.).

utils/  
• logger.py : Logger setup — writes logs to a file and to the console.  
• May contain a singleton.py or a function with LOCK_FILE to prevent two agents with the same AGENT_ID from running.

planner/   
• (If available) Extends the basic logic of scenarios, such as queue mode or action dependencies.  

roles/
• YAML behavior patterns for offline testing (if you do not connect to the server).

 run-lisa.ps1
• PowerShell script for running the agent locally with the necessary parameters.
It can be useful for CI/CD or manual startup.


agent.spec  
• PyInstaller configuration:  
• Specifies the main script (agent.py ).  
• Adds config/ and other folders to the exe.  
• Configures the --onefile, --noconsole options.  