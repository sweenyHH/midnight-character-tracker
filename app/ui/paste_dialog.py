from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QLabel, QLineEdit
)
import os
import re


class PasteDialog(QDialog):

    def __init__(self, target_folder):
        super().__init__()

        self.target_folder = target_folder

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
# VAULT INPUT FIELDS
# -------------------------------

        self.vault_inputs = {
            "row1": [],
            "row2": [],
            "row3": []
        }

        vault_layout = QVBoxLayout()

        for row_name in ["row1", "row2", "row3"]:
            row_layout = QHBoxLayout()

            label = QLabel(f"Vault Row {row_name[-1]}")
            row_layout.addWidget(label)

            for _ in range(3):
                field = QLineEdit()
                field.setPlaceholderText("100-999")
                field.setMaximumWidth(80)

                row_layout.addWidget(field)
                self.vault_inputs[row_name].append(field)

            vault_layout.addLayout(row_layout)

        layout.addLayout(vault_layout)

# -------------------------------
# Buttons
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
            print("[PasteDialog] No text provided.")
            return

# -------------------------------
# Extract character name
# -------------------------------

        match = re.search(r"Character:\s*(.+)", text)

        if match:
            full_name = match.group(1).strip()

# Keeps "-" and spaces, removes invalid filesystem characters

            safe_name = re.sub(r'[\\/*?:"<>|]', "_", full_name)

            file_name = f"{safe_name}.txt"
        else:

# Fallback 

            file_name = "unknown_character.txt"

# DEBUG to be deactivated or removed later

            print("[PasteDialog] WARNING: Could not extract character name.")

        full_path = os.path.join(self.target_folder, file_name)


# -------------------------------
# Collect vault data
# -------------------------------

        vault_lines = []

        for row_key, fields in self.vault_inputs.items():
            values = []

            for field in fields:
                text_val = field.text().strip()

                if text_val.isdigit():
                    num = int(text_val)

# enforce valid range

                    if 100 <= num <= 999:
                        values.append(str(num))

# Format line

            row_number = row_key[-1]
            line = f"Vault Row {row_number}: {', '.join(values)}"
            vault_lines.append(line)


# -------------------------------
# Inject vault data into text
# -------------------------------

            vault_block = "\n" + "\n".join(vault_lines) + "\n"

            text += "\n" + vault_block





# DEBUG deactivated, to be removed later

        # print(f"[DEBUG] Saving to: {full_path}")

# -------------------------------
# Save file (overwrite enabled)
# -------------------------------

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"[PasteDialog] Saved file: {full_path}")

# Close dialog

        self.accept()