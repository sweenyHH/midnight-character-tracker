# Main application window. Handles navigation between overview and detail view.

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import QTimer, Signal

from app.services.data_service import DataService
from app.ui.detail_view import DetailView
from app.utils.watcher import FolderWatcher
from app.utils.windows_to_import import WindowsToImportWatcher


class MainWindow(QMainWindow):

# Signal used to safely update UI from watcher thread

    files_changed_signal = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Midnight Character Tracker")
        self.setFixedSize(1800, 900)

# Set up DataService for handling parsed data

        self.data_service = DataService()

# Initialize watchers

        self.watcher = None
        self.win_to_import_watcher = None

# Connect signal to UI update method (thread-safe)

        self.files_changed_signal.connect(self._update_ui)

# Main layout container

        self.container = QWidget()
        self.layout = QVBoxLayout()

# Folder selection button

        self.select_button = QPushButton("Select Data Folder")
        self.select_button.clicked.connect(self.select_folder)

# Character overview table

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Character",
            "Class:",
            "Average Item Level:",
            "Level",
            "Specialization:"
        ])
        self.table.cellClicked.connect(self.open_character)

# Enable sorting

        self.table.setSortingEnabled(True)

# Detail view

        self.detail_view = DetailView()
        self.detail_view.hide()

# Back button for navigation

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.show_list)
        self.back_button.hide()

# Layout structure

        self.layout.addWidget(self.select_button)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.back_button)
        self.layout.addWidget(self.detail_view)

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

# --------------------------------------------------
# Folder selection
# --------------------------------------------------

    def select_folder(self):

# Opens a dialog for selecting the data folder.

        folder = QFileDialog.getExistingDirectory(self, "Select Folder")

        if folder:
            self.data_service.set_folder(folder)
            self.reload_list()
            self.start_watcher(folder)

# --------------------------------------------------
# Table handling
# --------------------------------------------------

    def reload_list(self):

# Reloads the overview table of characters.

        characters = self.data_service.get_characters()

        self.table.setRowCount(len(characters))

        for row, char in enumerate(characters):

# Helper function to safely access dictionary values

            def get_value(key):
                return char.location.get(key, "-")

# Fill table columns

            self.table.setItem(row, 0, QTableWidgetItem(char.name))
            self.table.setItem(row, 1, QTableWidgetItem(get_value("Class")))
            self.table.setItem(row, 2, QTableWidgetItem(get_value("Average Item Level")))
            self.table.setItem(row, 3, QTableWidgetItem(get_value("Level")))
            self.table.setItem(row, 4, QTableWidgetItem(get_value("Specialization")))

# Resize columns automatically for better layout

        self.table.resizeColumnsToContents()

    def open_character(self, row, column):

# Opens detail view for selected character based on clicked row.

        character = self.data_service.get_characters()[row]

        self.detail_view.set_character(character)

        self.table.hide()
        self.back_button.show()
        self.detail_view.show()

    def show_list(self):

# Returns to the overview table.

        self.detail_view.hide()
        self.back_button.hide()
        self.table.show()

# --------------------------------------------------
# Watcher management
# --------------------------------------------------

    def start_watcher(self, folder):

# Starts both watchers (import + folder watcher).

        print("Starting watchers...")

# Stop existing watchers if running

        if self.watcher:
            print("Stopping FolderWatcher")
            self.watcher.stop()

        if self.win_to_import_watcher:
            print("Stopping WindowsToImportWatcher")
            self.win_to_import_watcher.stop()

# Start watcher for import folder

        self.watcher = FolderWatcher(folder, self.on_files_changed)
        self.watcher.start()
        print("FolderWatcher started")

# Start Windows → Linux transfer watcher

        self.win_to_import_watcher = WindowsToImportWatcher()
        self.win_to_import_watcher.start()
        print("WindowsToImportWatcher started")

    def on_files_changed(self):

# Called by watcher (from another thread).
# Uses Qt signal to safely trigger UI update in main thread.

# Debug output

        print("DEBUG: on_files_changed triggered")

# Emit signal → ensures UI execution

        self.files_changed_signal.emit()

    def _update_ui(self):

# Runs in Qt main thread → safe UI update.

        print("Files changed -> waiting before reload")

        import time

# Sleep needed to wait for filesystem to fully update

        time.sleep(1.0)

        print("Now reloading data")

        self.data_service.load_data()
        self.reload_list()

# --------------------------------------------------
# Clean shutdown 
# --------------------------------------------------

    def closeEvent(self, event):

# Ensures watchers are properly stopped when the application closes.

        print("Shutting down watchers...")

        if self.watcher:
            self.watcher.stop()

        if self.win_to_import_watcher:
            self.win_to_import_watcher.stop()

        event.accept()
