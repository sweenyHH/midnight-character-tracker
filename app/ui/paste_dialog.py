from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QLabel   
)
from app.utils.app_paths import get_import_dir 
import os
import re

from app.utils.logger import logger

# import safe write function
from app.storage.user_data_storage import extract_user_data


def write_character_file_with_user_data(path, new_content):

    existing_lines = []

    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            existing_lines = f.readlines()

    user_block = extract_user_data(existing_lines)

    with open(path, "w", encoding="utf-8") as f:

# write fresh imported content
        f.write(new_content.rstrip() + "\n\n")

# re-append user data block
        if user_block:
            f.writelines(user_block)



class PasteDialog(QDialog):


    def __init__(self):
        super().__init__()

        self.target_folder = str(
            get_import_dir()
        )

        self.setWindowTitle("Paste Character Data")
        self.setMinimumSize(700, 500)

        layout = QVBoxLayout()

        label = QLabel("Paste your character export here:")
        layout.addWidget(label)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Paste your WoW export text here...")
        self.text_edit.setFocus()
        layout.addWidget(self.text_edit)

# -------------------------------
# BUTTONS
# -------------------------------
        button_layout = QHBoxLayout()

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_text)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

# --------------------------------------------------
# SAVE LOGIC
# --------------------------------------------------
    def save_text(self):
        text = self.text_edit.toPlainText().strip()

        if not text:

            logger.warning(
                "Paste dialog save attempted with empty text"
            )

            print("[PasteDialog] No text provided.")
            return

# -------------------------------
# Extract character name
# -------------------------------
        match = re.search(r"Character:\s*(.+)", text)

        if match:
            full_name = match.group(1).strip()

            logger.info(
                f"Character import detected: "
                f"{full_name}"
            )

# sanitize filename
            safe_name = re.sub(r'[\\/*?:"<>|]', "_", full_name)
            file_name = f"{safe_name}.txt"

        else:

            file_name = "unknown_character.txt"

            logger.warning(
                "Character import failed to extract character name"
            )

            print(
                "[PasteDialog] WARNING: "
                "Could not extract character name."
            )

        full_path = os.path.join(self.target_folder, file_name)

# -------------------------------
# SAVE FILE (SAFE OVERWRITE)
# -------------------------------

        try:

            write_character_file_with_user_data(
                full_path,
                text
            )

            logger.info(
                f"Character import saved: "
                f"{full_path}"
            )

            self.accept()

        except Exception:

            logger.exception(
                f"Character import failed: "
                f"{full_path}"
            )

            raise

