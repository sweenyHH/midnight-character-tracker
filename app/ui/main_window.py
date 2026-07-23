from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox
from app.services.data_service import DataService
from app.ui.detail_view import DetailView
from app.ui.character_table import CharacterTable
from app.ui.top_panel import TopPanel

from app.ui.paste_dialog import PasteDialog
from app.app_info import APP_NAME
from app.storage.character_file_storage import (
    delete_character_file,
)
from app.utils.logger import logger
from app.utils.app_paths import get_import_dir
from app.services.refresh_service import RefreshService
from app.localization.ui_strings import get_ui_string

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setObjectName("mainWindow")

        self.setWindowTitle(APP_NAME)
        self.resize(1800, 900)
        self.setMinimumSize(1400, 800)

        logger.info("MainWindow initialized")

        self.data_service = DataService()

        self.refresh_service = RefreshService(
            self.data_service
        )

        self.table = CharacterTable()
        self.table.setObjectName("characterList")
        self.table.cellClicked.connect(self.open_character)

        self.detail_view = DetailView()
        self.detail_view.setObjectName("detailView")

        self.detail_view.hide()

        self.current_character = None
        
        self.top_panel = TopPanel(
            self.open_paste_dialog,
            self.show_list,
            self.open_warband_tasks
        )
        self.top_panel.setObjectName("topPanel")

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

        container.setObjectName("mainContainer")
        container.setLayout(layout)
        self.setCentralWidget(container)

        default_folder = str(get_import_dir())

        self.data_service.set_folder(default_folder)

        self.reload_all()


# --------------------------------------------------

    def reload_all(self):

        logger.info("Reloading all data")

        result = (self.refresh_service.execute_refresh(self.current_character))

        if result is None:
            return

        logger.info(
        f"Loaded {len(result.characters)} characters"
        )
        
        self.table.load_characters(result.characters)


        self.top_panel.update_reputation(
            result.reputations,
            result.currency_totals,
        )

# Refresh currently open detail view

        
        self.current_character = (
            result.selected_character
        )

        if result.selected_character is not None:
            self.detail_view.set_character(
                result.selected_character
            )



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

        # Refresh data after leaving the character detail view 
        self.reload_all()

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
            get_ui_string(
                "delete_character"
            ),
            get_ui_string(
                "delete_character_confirmation"
            ).format(
                name=character.name
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
     
 
    def closeEvent(self, event):

        logger.info(
            "Application closing"
        )

        event.accept()

