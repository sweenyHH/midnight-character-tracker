# Main application window. Handles navigation between overview and detail view.

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel
)
from PySide6.QtCore import QTimer, Signal, Qt

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


# Apply dark styling to button

        self.select_button.setStyleSheet("""
        QPushButton {
                background-color: #3c3f41;
                color: white;
                border: 1px solid #555;
                padding: 6px;
        }
        QPushButton:hover {
                background-color: #484a4c;
        }
        """)



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

# --------------------------------------------------
# New layout structure (top boxes + bottom table area)
# --------------------------------------------------

# Top container (holds Box1 and Box2 - 20% of window height)

        self.top_container = QWidget()
        self.top_layout = QHBoxLayout()

# Box 1 container (left side, will hold button + label)

        self.box1_container = QWidget()
        self.box1_layout = QVBoxLayout()

# Box 1 label

        self.box1_label = QLabel("Box 1")
        self.box1_label.setAlignment(Qt.AlignCenter)

# Add button and label to Box 1 (button on top)

        self.box1_layout.addWidget(self.select_button)
        self.box1_layout.addWidget(self.box1_label)

        self.box1_container.setLayout(self.box1_layout)
        
        self.box1_container.setStyleSheet("""
        background-color: #2b2b2b;
        color: #ffffff;
        border: 1px solid #444;
        """)


# Box 2 (right side, text only)

        self.box2 = QLabel("Box 2")
        self.box2.setAlignment(Qt.AlignCenter)
        
        self.box2.setStyleSheet("""
        background-color: #2b2b2b;
        color: #ffffff;
        border: 1px solid #444;
        """)


# Add boxes to top layout (equal width)

        self.top_layout.addWidget(self.box1_container)
        self.top_layout.addWidget(self.box2)

        self.top_container.setLayout(self.top_layout)

# Bottom container (holds existing UI elements - 80% of window height)

        self.bottom_container = QWidget()
        self.bottom_layout = QVBoxLayout()

# Keep original widgets inside bottom area (button removed from here)

        self.bottom_layout.addWidget(self.table)
        self.bottom_layout.addWidget(self.back_button)
        self.bottom_layout.addWidget(self.detail_view)

        self.bottom_container.setLayout(self.bottom_layout)

# Add both sections to main layout with proportion (20% / 80%)

        self.layout.addWidget(self.top_container, 2)
        self.layout.addWidget(self.bottom_container, 8)

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

# Updates Box 2 with latest reputation data

    def update_reputation_box(self):

        reputation_list = self.data_service.get_reputation()

        if not reputation_list:
            self.box2.setText("No reputation data available")
            return

# Build HTML string (centered title, left-aligned content)

        text = "<h3 style='text-align:center;'>Reputation</h3>"
        text += "<div style='text-align:left;'>"

        for rep in reputation_list:

# Case 1: Renown reputations

            if rep.rep_type == "renown":
                text += f"<b>{rep.name}</b>: Renown {rep.level}<br>"

# Case 2: Standard reputations

            else:
                if rep.current is not None and rep.maximum is not None:
                    text += f"<b>{rep.name}</b>: {rep.level} ({rep.current}/{rep.maximum})<br>"
                else:
                    text += f"<b>{rep.name}</b>: {rep.level}<br>"

        text += "</div>"

        self.box2.setText(text)



# --------------------------------------------------
# Folder selection
# --------------------------------------------------

    def select_folder(self):

# Opens a dialog for selecting the data folder.

        folder = QFileDialog.getExistingDirectory(self, "Select Folder")

        if folder:
            self.data_service.set_folder(folder)
            self.reload_list()
            self.update_reputation_box()
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
        self.update_reputation_box()

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