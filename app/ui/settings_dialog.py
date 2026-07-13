from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QRadioButton,
    QPushButton,
    QHBoxLayout,
    QApplication,
    QButtonGroup,
)

from PySide6.QtCore import Signal

from app.storage.settings_storage import (
    load_setting,
    save_setting,
)
from app.utils.logger import logger, LOG_DIR
from app.ui.theme_manager import ThemeManager
import os
import platform
import subprocess

class SettingsDialog(QDialog):

    settings_saved = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.resize(350, 250)

        layout = QVBoxLayout(self)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

        title = QLabel("Application Settings")
        title.setObjectName("settingsTitle")

        layout.addWidget(title)

# --------------------------------------------------
# THEME
# --------------------------------------------------

        layout.addWidget(QLabel("<b>Theme</b>"))

        self.dark_radio = QRadioButton("Dark")
        self.light_radio = QRadioButton("Light")
        self.wow_radio = QRadioButton("WoW")
        self.modern_radio = QRadioButton("Modern")

        self.theme_group = QButtonGroup(self)

        self.theme_group.addButton(
            self.dark_radio
        )

        self.theme_group.addButton(
            self.light_radio
        )

        self.theme_group.addButton(
            self.wow_radio
        )

        self.theme_group.addButton(
            self.modern_radio
        )

        layout.addWidget(self.dark_radio)
        layout.addWidget(self.light_radio)
        layout.addWidget(self.wow_radio)
        layout.addWidget(self.modern_radio)


# --------------------------------------------------
# Number Format
# --------------------------------------------------

        layout.addWidget(
            QLabel("<b>Number Format</b>")
        )

        self.german_numbers = QRadioButton(
            "German (1.234.567)"
        )

        self.english_numbers = QRadioButton(
            "English (1,234,567)"
        )

        self.number_format_group = QButtonGroup(self)

        self.number_format_group.addButton(
            self.german_numbers
        )

        self.number_format_group.addButton(
            self.english_numbers
        )

        layout.addWidget(
            self.german_numbers
        )

        layout.addWidget(
            self.english_numbers
        )


# --------------------------------------------------
# LOGS
# --------------------------------------------------

        logs_button = QPushButton("Open Log Folder")
        logs_button.clicked.connect(
            self._open_log_folder
        )

        layout.addWidget(logs_button)

# --------------------------------------------------
# LOAD CURRENT THEME SETTING
# --------------------------------------------------

        current_theme = load_setting(
            "theme",
            "dark"
        )

        if current_theme == "dark":
            self.dark_radio.setChecked(True)

        elif current_theme == "light":
            self.light_radio.setChecked(True)

        elif current_theme == "wow":
            self.wow_radio.setChecked(True)

        elif current_theme == "modern":
            self.modern_radio.setChecked(True)

# --------------------------------------------------
# LOAD NUMBER FORMAT
# --------------------------------------------------

        current_number_format = load_setting(
            "number_format",
            "german"
        )

        if current_number_format == "english":

            self.english_numbers.setChecked(
                True
            )

        else:

            self.german_numbers.setChecked(
                True
            )

# --------------------------------------------------
# BUTTONS
# --------------------------------------------------

        button_row = QHBoxLayout()

        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")

        save_button.clicked.connect(
            self._save_settings
        )

        cancel_button.clicked.connect(
            self.reject
        )

        button_row.addStretch()
        button_row.addWidget(save_button)
        button_row.addWidget(cancel_button)

        layout.addStretch()
        layout.addLayout(button_row)

# --------------------------------------------------
# OPEN LOG FOLDER
# --------------------------------------------------

    def _open_log_folder(self):

        log_path = str(LOG_DIR.resolve())

        try:

            logger.info(
                "Log folder opened"
            )

            system = platform.system()

            # -----------------------------
            # Windows
            # -----------------------------
            if system == "Windows":

                os.startfile(log_path)

            # -----------------------------
            # macOS
            # -----------------------------
            elif system == "Darwin":

                subprocess.Popen(
                    ["open", log_path]
                )

            # -----------------------------
            # Linux / WSL
            # -----------------------------
            else:

                # Detect WSL
                with open(
                    "/proc/version",
                    "r",
                    encoding="utf-8"
                ) as f:

                    version_info = f.read().lower()

                # WSL
                if "microsoft" in version_info:

                    subprocess.Popen(
                        ["explorer.exe", "."],
                        cwd=log_path
                    )

                # Native Linux
                else:

                    subprocess.Popen(
                        ["xdg-open", log_path]
                    )

        except Exception:

            logger.exception(
                "Failed to open log folder"
            )


# --------------------------------------------------
# SAVE
# --------------------------------------------------

    def _save_settings(self):

        if self.dark_radio.isChecked():
            theme = "dark"

        elif self.light_radio.isChecked():
            theme = "light"

        elif self.wow_radio.isChecked():
            theme = "wow"

        else:
            theme = "modern"

        save_setting(
            "theme",
            theme
        )

        ThemeManager.load_theme(
            QApplication.instance(),
            theme
        )


        if self.english_numbers.isChecked():

            save_setting(
                "number_format",
                "english"
            )

        else:

            save_setting(
                "number_format",
                "german"
            )

        self.settings_saved.emit()

        self.accept()