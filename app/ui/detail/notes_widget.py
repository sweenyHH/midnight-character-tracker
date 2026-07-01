from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
import os


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
        self.textbox.textChanged.connect(self._save_notes)

        self.current_file = None

# --------------------------------------------------
# SET CHARACTER
# --------------------------------------------------
    def set_character(self, character):

        self.current_file = character.source_file

        self.textbox.blockSignals(True)
        self.textbox.setPlainText(self._load_notes(self.current_file))
        self.textbox.blockSignals(False)

# --------------------------------------------------
# LOAD NOTES (FROM USER BLOCK)
# --------------------------------------------------
    def _load_notes(self, file_path):

        if not file_path or not os.path.exists(file_path):
            return ""

        notes = []
        in_user_block = False
        in_notes = False

        with open(file_path, encoding="utf-8") as f:
            for line in f:

                stripped = line.strip()

                if stripped == "### USER_DATA_START ###":
                    in_user_block = True
                    continue

                if stripped == "### USER_DATA_END ###":
                    break

                if in_user_block and stripped == "Notes:":
                    in_notes = True
                    continue

                if in_notes:
                    if stripped.endswith(":") and stripped != "Notes:":
                        break
                    notes.append(line.rstrip())

        return "\n".join(notes).strip()

# --------------------------------------------------
# SAVE NOTES (MERGE SAFE)
# --------------------------------------------------
    def _save_notes(self):

        if not self.current_file or not os.path.exists(self.current_file):
            return

        with open(self.current_file, encoding="utf-8") as f:
            lines = f.readlines()

        text = self.textbox.toPlainText().strip()

# -------------------------------
# EXTRACT EXISTING USER DATA
# -------------------------------
        in_user_block = False
        existing_duties = []

        new_lines = []

        for line in lines:
            stripped = line.strip()

            if stripped == "### USER_DATA_START ###":
                in_user_block = True
                continue

            if stripped == "### USER_DATA_END ###":
                in_user_block = False
                continue

            if in_user_block:
                # preserve WeeklyDuties
                if stripped.startswith("WeeklyDuties:") or "=" in stripped:
                    existing_duties.append(line)
                    continue

                # skip existing notes
            else:
                new_lines.append(line)

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