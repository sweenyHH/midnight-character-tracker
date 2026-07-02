from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QVBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.storage.user_data_storage import load_section


class VaultTab(QWidget):

    def set_character(self, character):

        # -------------------------------
        # CLEAN OLD LAYOUT
        # -------------------------------
        old_layout = self.layout()

        if old_layout:
            while old_layout.count():
                item = old_layout.takeAt(0)

                if item.widget():
                    item.widget().deleteLater()

        # -------------------------------
        # ROOT LAYOUT
        # -------------------------------
        root = QVBoxLayout()
        root.setContentsMargins(20, 20, 20, 20)
        self.setLayout(root)

        grid = QGridLayout()
        grid.setSpacing(20)
        root.addLayout(grid, 1)

        # -------------------------------
        # LOAD VAULT DATA FROM STORAGE
        # -------------------------------
        vault = {
            "row1": [],
            "row2": [],
            "row3": [],
        }

        file_path = getattr(character, "source_file", None)

        if file_path:

            for line in load_section(file_path, "Vault"):

                if "=" not in line:
                    continue

                key, value = line.split("=", 1)

                row, col = key.split("_")
                row_name = f"row{int(row) + 1}"

                while len(vault[row_name]) <= int(col):
                    vault[row_name].append(None)

                vault[row_name][int(col)] = value

        # -------------------------------
        # BOX CREATOR
        # -------------------------------
        def create_box(value):

            lbl = QLabel(str(value))
            lbl.setAlignment(Qt.AlignCenter)

            lbl.setMinimumSize(140, 100)
            lbl.setSizePolicy(
                QSizePolicy.Expanding,
                QSizePolicy.Expanding
            )

            lbl.setObjectName("vaultBox")

            return lbl

        # -------------------------------
        # FILL ROW
        # -------------------------------
        def fill_row(row_index, values):

            values = values[:3]

            for col in range(3):
                val = (
                    values[col]
                    if col < len(values) and values[col]
                    else "-"
                )

                grid.addWidget(
                    create_box(val),
                    row_index,
                    col + 1
                )

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
            label.setAlignment(
                Qt.AlignRight | Qt.AlignVCenter
            )


            label.setObjectName("vaultRowLabel")

            grid.addWidget(label, row_index, 0)

            fill_row(
                row_index,
                vault.get(key, [])
            )

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

