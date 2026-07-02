from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PySide6.QtCore import QTimer
import os


from app.storage.user_data_storage import (
    load_section,
    save_section,
)

class NotesWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

# spacing
        self.layout.setSpacing(8)

        self.layout.addWidget(QLabel("<b>Notes</b>"))

        self.textbox = QTextEdit()

# disable rich text
        self.textbox.setAcceptRichText(False)

        self.textbox.setPlaceholderText("Enter notes (max 512 characters)...")

        self.layout.addWidget(self.textbox)

        self.textbox.textChanged.connect(self._limit_length)
        
        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self._save_notes)

        self.textbox.textChanged.connect(self._schedule_save)


        self.current_file = None

# --------------------------------------------------
# SET CHARACTER
# --------------------------------------------------
    def set_character(self, character):

        self.current_file = character.source_file

        
        new_text = self._load_notes(self.current_file)

        if new_text != self.textbox.toPlainText():
            self.textbox.blockSignals(True)
            self.textbox.setPlainText(new_text)
            self.textbox.blockSignals(False)

# --------------------------------------------------
# LOAD NOTES (FROM USER BLOCK)
# --------------------------------------------------

    def _load_notes(self, file_path):

        lines = load_section(
            file_path,
            "Notes"
        )

        return "\n".join(lines).strip()


# --------------------------------------------------
# SAVE NOTES (MERGE SAFE)
# --------------------------------------------------

    def _schedule_save(self):

        self.save_timer.start(3000)

    def _save_notes(self):

        if not self.current_file:
            return

        text = self.textbox.toPlainText().strip()

        note_lines = []

        if text:
            note_lines = text.splitlines()

        save_section(
            self.current_file,
            "Notes",
            note_lines
        )

# -------------------------------
# BUILD NEW USER BLOCK
# -------------------------------
        user_block = []

        if text or existing_duties:

            user_block.append("### USER_DATA_START ###\n")

            if text:
                user_block.append("Notes:\n")
                user_block.append(text + "\n")

            if existing_duties:
                user_block.append("WeeklyDuties:\n")

                for line in existing_duties:
                    if "=" in line:
                        user_block.append(line)

            user_block.append("### USER_DATA_END ###\n")

# -------------------------------
# WRITE FILE
# -------------------------------
        with open(self.current_file, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

            if user_block:
                f.write("\n")
                f.writelines(user_block)

# --------------------------------------------------
# LIMIT LENGTH
# --------------------------------------------------
    def _limit_length(self):

        text = self.textbox.toPlainText()

        if len(text) > 512:
            self.textbox.blockSignals(True)
            self.textbox.setPlainText(text[:512])

            cursor = self.textbox.textCursor()
            cursor.setPosition(len(text[:512]))
            self.textbox.setTextCursor(cursor)

            self.textbox.blockSignals(False)