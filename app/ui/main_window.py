from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox
from PySide6.QtCore import Signal
from app.services.data_service import DataService
from app.ui.detail_view import DetailView
from app.ui.character_table import CharacterTable
from app.ui.top_panel import TopPanel
from app.utils.watcher import FolderWatcher
from app.ui.paste_dialog import PasteDialog
from app.app_info import APP_NAME
from app.storage.character_file_storage import (
    delete_character_file,
)
from app.utils.logger import logger
from app.utils.app_paths import get_import_dir
from app.services.warband_currency_service import (
    get_warband_currency_totals
)


class MainWindow(QMainWindow):

    files_changed_signal = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setFixedSize(1800, 900)

        logger.info("MainWindow initialized")

        self.data_service = DataService()

        self.table = CharacterTable()
        self.table.cellClicked.connect(self.open_character)

        self.detail_view = DetailView()
        self.detail_view.hide()

        self.current_character = None
        
        self.top_panel = TopPanel(
            self.open_paste_dialog,
            self.show_list,
            self.open_warband_tasks
        )

        self.top_panel.settings_changed.connect(
            self.reload_all
        )

        self.table.character_delete_requested.connect(
            self.delete_character
        )

        layout = QVBoxLayout()
        layout.addWidget(self.top_panel)
        layout.addWidget(self.table)
        layout.addWidget(self.detail_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.files_changed_signal.connect(self._update_ui)

        default_folder = str(get_import_dir())

        self.data_service.set_folder(default_folder)

        self.start_watcher(default_folder)

        self.reload_all()


# --------------------------------------------------

    def reload_all(self):

        logger.info("Reloading all data")

        self.data_service.load_data()

        characters = self.data_service.get_characters()

        currency_totals = (
            get_warband_currency_totals(
                characters
            )
        )

        logger.info(
        f"Loaded {len(characters)} characters"
        )
        
        self.table.load_characters(characters)
        self.top_panel.update_reputation(
            self.data_service.get_top_reputations(),
            currency_totals
        )

# Refresh currently open detail view
        if self.current_character is not None:
            self.detail_view.set_character(self.current_character)


# --------------------------------------------------

    def open_character(self, row, _):

        logger.info(
            f"Opening character row: {row}"
        )

        char = self.table.item(row, 0).data(0x0100)

        logger.info(
            f"Character selected: {char.name}"
        )

        self.current_character = char

        logger.info(
            "Starting DetailView update"
        )

        self.detail_view.set_character(char)

        logger.info(
            "DetailView update finished"
        )

        logger.info(
            "Switching UI to detail view"
        )

        self.table.hide()
        self.detail_view.show()
        self.top_panel.back_btn.show()

        logger.info(
            "Detail view displayed"
        )

    def show_list(self):

        logger.info(
            "Returned to character list"
        )

        self.detail_view.hide()
        self.table.show()
        self.top_panel.back_btn.hide()

# --------------------------------------------------
 
    def open_paste_dialog(self):

        logger.info(
          "Opening paste dialog"
        )

        dialog = PasteDialog()
        dialog.exec()

        self.reload_all()

# --------------------------------------------------

    def open_warband_tasks(self):

        logger.info(
          "Opening Warband Tasks dialog"
        )

        from app.ui.warband_task_dialog import (
            WarbandTaskDialog
        )

        dialog = WarbandTaskDialog(self)
        dialog.exec()

        self.reload_all()

# --------------------------------------------------

    def delete_character(self, character):

        result = QMessageBox.question(
            self,
            "Delete Character",
            (
                f'Delete "{character.name}"?\n\n'
                "This will permanently remove "
                "the character export file."
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if result != QMessageBox.Yes:
            return

        if delete_character_file(character):

            logger.info(
             f"Character deleted: {character.name}"
            )

            self.current_character = None

            self.reload_all()

            self.show_list()

# --------------------------------------------------
        
    def start_watcher(self, folder):
        self.watcher = FolderWatcher(
            folder,
            self.files_changed_signal.emit
        )
        self.watcher.start()

    def _update_ui(self):

        logger.info(
            "Watcher triggered UI update START"
        )

        import time
        time.sleep(1.0)
        self.reload_all()

        logger.info(
            "Watcher triggered UI update END"
        )

    def closeEvent(self, event):

        logger.info(
            "Application closing"
        )

        if hasattr(self, "watcher"):
            self.watcher.stop()

        event.accept()

