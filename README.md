# LISA Windows agent

## Description

WinAgent is a cross-platform user activity simulator for Windows systems, designed to emulate human-like interactions
with applications, browsers, and system tools.

## Features

-Launching and managing Windows applications.  
-Randomized behavior – Actions can be randomized to make them more human-like.  
-Python script – runs directly through agent.py.
-Flexible configuration, YAML role templates are used.

## Structure

    WinAgent/
        ├── actions/        # Logic of actions: launching applications, browser, terminals, etc.
        ├── agent.py        # Main executable agent: loop, scheduler, server integration
        ├── agent.spec      # PyInstaller build configuration for creating .exe
        ├── agent_OLD.py    # The agent's old backup, can be deleted or archived
        ├── client/         # Working with the LISA server: API requests (config, status, logs)
        ├── config/         # Local YAML configs: settings.yaml, paths.yaml, etc.
        ├── planner/        # Scheduler (if there is an extension of the script logic)
        ├── roles/          # YAML templates for offline behavior (if the server is not used)
        ├── run-lisa.ps1    # PowerShell script for launching or testing the agent manually
        ├── utils/          # Logger and auxiliary utilities: singleton lock and setup_logger
        ├── .venv/          # Python virtual environment
        ├── .git/, .idea/   # Git and IDE configs (PyCharm)


