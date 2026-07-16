# Midnight Character Tracker

Purpose:
Desktop companion application for World of Warcraft characters.

Tech Stack:
- Python
- PySide6
- PyInstaller

Architecture:
- MainWindow
- DetailView
- TopPanel
- CharacterTable
- User data stored in character files

Key Features:
- Character Import
- Character Deletion
- Notes
- Weekly Duties
- Vault Progress
- Warband Tasks
- Themes

Important Architecture Decisions:
- No file watcher
- Explicit refresh flow
- Persistent UI widgets
- Local data storage

Documentation:
- docs/architecture/
- docs/user-guide/