from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QGridLayout, QLineEdit, QPushButton
)
from PySide6.QtCore import Qt
import os


class VaultProgressWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("<b>Vault Progress</b>"))

        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)

        self.fields = {}  # (row, col) → QLineEdit

        row_labels = ["Raid Slots", "M+ Slots", "Delve Slots"]

        for row in range(3):
            label = QLabel(row_labels[row])
            self.grid.addWidget(label, row, 0)

            for col in range(3):
                field = QLineEdit()
                field.setMaximumWidth(60)
                field.setPlaceholderText("...")
                field.setAlignment(Qt.AlignCenter)
                field.setMaxLength(3)


                field.textChanged.connect(self._save)

                self.grid.addWidget(field, row, col + 1)
                self.fields[(row, col)] = field

        self.grid.setColumnStretch(0, 1)

# Clear button
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.clear_all)
        self.layout.addWidget(self.clear_btn)

        self.current_file = None

# --------------------------------------------------
    def set_character(self, character):

        self.current_file = character.source_file

        data = self._load()

        for (row, col), field in self.fields.items():
            key = f"{row}_{col}"
            field.blockSignals(True)
            field.setText(data.get(key, ""))
            field.blockSignals(False)

# --------------------------------------------------
    def clear_all(self):

        for field in self.fields.values():
            field.setText("")

        self._save()

# --------------------------------------------------
# LOAD (USER BLOCK)
# --------------------------------------------------
    def _load(self):

        result = {}

        if not self.current_file or not os.path.exists(self.current_file):
            return result

        in_user_block = False
        in_vault = False

        with open(self.current_file, encoding="utf-8") as f:
            for line in f:

                stripped = line.strip()

                if stripped == "### USER_DATA_START ###":
                    in_user_block = True
                    continue

                if stripped == "### USER_DATA_END ###":
                    break

                if in_user_block and stripped == "Vault:":
                    in_vault = True
                    continue

                if in_vault:
                    if "=" in stripped:
                        k, v = stripped.split("=")
                        result[k] = v
                    elif stripped.endswith(":"):
                        break

        return result

# --------------------------------------------------
# SAVE (MERGE SAFE)
# --------------------------------------------------
    def _save(self):

        if not self.current_file or not os.path.exists(self.current_file):
            return

        with open(self.current_file, encoding="utf-8") as f:
            lines = f.readlines()

# extract existing USER data
        in_user_block = False

        notes_lines = []
        duties_lines = []
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
                if stripped.startswith("Notes:") or notes_lines:
                    notes_lines.append(line)
                    continue

                if stripped.startswith("WeeklyDuties:") or "=" in stripped:
                    duties_lines.append(line)
                    continue

            else:
                new_lines.append(line)

# build vault data
        vault_lines = []
        for (row, col), field in self.fields.items():
            value = field.text().strip()
            if value:
                vault_lines.append(f"{row}_{col}={value}\n")

# rebuild USER block
        user_block = []

        if notes_lines or duties_lines or vault_lines:

            user_block.append("### USER_DATA_START ###\n")

            if notes_lines:
                user_block.extend(notes_lines)

            if duties_lines:
                user_block.extend(duties_lines)

            if vault_lines:
                user_block.append("Vault:\n")
                user_block.extend(vault_lines)

            user_block.append("### USER_DATA_END ###\n")

# write file
        with open(self.current_file, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

            if user_block:
                f.write("\n")
                f.writelines(user_block)