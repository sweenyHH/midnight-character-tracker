from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import os


class VaultTab(QWidget):

    def set_character(self, character):

# -------------------------------
# ROOT LAYOUT
# -------------------------------
        root = QVBoxLayout()
        root.setContentsMargins(20, 20, 20, 20)
        self.setLayout(root)

        grid = QGridLayout()
        grid.setSpacing(20)
        root.addLayout(grid, 1)

# DEFAULT (parsed data)
        vault = getattr(character, "vault", {
            "row1": [],
            "row2": [],
            "row3": []
        })

# ==================================================
# LOAD USER DATA OVERRIDE
# ==================================================
        user_vault = {"row1": [], "row2": [], "row3": []}

        file_path = getattr(character, "source_file", None)

        if file_path and os.path.exists(file_path):

            in_user_block = False
            in_vault = False

            with open(file_path, encoding="utf-8") as f:
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
                            key, value = stripped.split("=")

                            row, col = key.split("_")
                            row_name = f"row{int(row) + 1}"

                            # ensure list size
                            while len(user_vault[row_name]) <= int(col):
                                user_vault[row_name].append(None)

                            user_vault[row_name][int(col)] = value

                        elif stripped.endswith(":"):
                            break

#  Use user data if available
        if any(user_vault[r] for r in user_vault):
            vault = user_vault

# -------------------------------
# BOX CREATOR 
# -------------------------------
        def create_box(value):
            lbl = QLabel(str(value))
            lbl.setAlignment(Qt.AlignCenter)

            lbl.setMinimumSize(140, 100)
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            font = QFont()
            font.setPointSize(16)
            font.setBold(True)
            lbl.setFont(font)

            lbl.setStyleSheet("""
                border: 2px solid #666;
                border-radius: 10px;
                background-color: #222;
                padding: 10px;
            """)

            return lbl

# -------------------------------
# FILL ROW
# -------------------------------
        def fill_row(row_index, values):
            values = values[:3]

            for col in range(3):
                val = values[col] if col < len(values) and values[col] else "-"
                grid.addWidget(create_box(val), row_index, col + 1)

# -------------------------------
# LABELS
# -------------------------------
        labels = [
            ("Raid Slots", "row1"),
            ("M+ Slots", "row2"),
            ("Delve Slots", "row3"),
        ]

        for row_index, (label_text, key) in enumerate(labels):

            label = QLabel(label_text)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            font = QFont()
            font.setPointSize(14)
            font.setBold(True)
            label.setFont(font)

            grid.addWidget(label, row_index, 0)

            fill_row(row_index, vault.get(key, []))

# -------------------------------
# GRID STRETCH
# -------------------------------
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 2)
        grid.setColumnStretch(2, 2)
        grid.setColumnStretch(3, 2)

        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setRowStretch(2, 1)

