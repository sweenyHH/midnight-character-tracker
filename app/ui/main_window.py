from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Signal

from app.services.data_service import DataService
from app.ui.detail_view import DetailView
from app.ui.character_table import CharacterTable
from app.ui.top_panel import TopPanel
from app.utils.watcher import FolderWatcher
from app.utils.windows_to_import import WindowsToImportWatcher
from app.ui.paste_dialog import PasteDialog

import os


class MainWindow(QMainWindow):

    files_changed_signal = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Midnight Character Tracker")
        self.setFixedSize(1800, 900)

        self.data_service = DataService()

        self.table = CharacterTable()
        self.table.cellClicked.connect(self.open_character)

        self.detail_view = DetailView()
        self.detail_view.hide()

        self.top_panel = TopPanel(
            self.select_folder,
            self.open_paste_dialog,
            self.show_list
        )

        layout = QVBoxLayout()
        layout.addWidget(self.top_panel)
        layout.addWidget(self.table)
        layout.addWidget(self.detail_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.files_changed_signal.connect(self._update_ui)

        default_folder = os.path.join(os.getcwd(), "import")

        if os.path.exists(default_folder):
            self.data_service.set_folder(default_folder)
            self.reload_all()

# --------------------------------------------------

    def reload_all(self):

        self.data_service.load_data()

        characters = self.data_service.get_characters()
        print("DEBUG characters count:", len(characters))

        self.table.load_characters(characters)
        self.top_panel.update_reputation(self.data_service.get_top_reputations())

# --------------------------------------------------

    def open_character(self, row, _):
        char = self.table.item(row, 0).data(0x0100)

        self.detail_view.set_character(char)

        self.table.hide()
        self.detail_view.show()
        self.top_panel.back_btn.show()

    def show_list(self):
        self.detail_view.hide()
        self.table.show()
        self.top_panel.back_btn.hide()

# --------------------------------------------------

    def open_paste_dialog(self):
        dialog = PasteDialog(self.data_service.folder_path)
        dialog.exec()
        self.reload_all()

    def select_folder(self):
        from PySide6.QtWidgets import QFileDialog

        folder = QFileDialog.getExistingDirectory(self, "Select Folder")

        if folder:
            self.data_service.set_folder(folder)
            self.reload_all()
            self.start_watcher(folder)

# --------------------------------------------------

    def start_watcher(self, folder):
        self.watcher = FolderWatcher(folder, self.files_changed_signal.emit)
        self.watcher.start()

        self.win_to_import_watcher = WindowsToImportWatcher()
        self.win_to_import_watcher.start()

    def _update_ui(self):
        import time
        time.sleep(1.0)
        self.reload_all()

    def closeEvent(self, event):
        if hasattr(self, "watcher"):
            self.watcher.stop()
        if hasattr(self, "win_to_import_watcher"):
            self.win_to_import_watcher.stop()
        event.accept()
