
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QVBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import Qt

from app.storage.user_data_storage import load_section


class VaultTab(QWidget):

    def __init__(self):
        super().__init__()

        # -------------------------------
        # ROOT LAYOUT (CREATE ONCE)
        # -------------------------------
        self.root = QVBoxLayout(self)

        self.root.setContentsMargins(
            20,
            20,
            20,
            20
        )

        self.grid = QGridLayout()
        self.grid.setSpacing(20)

        self.root.addLayout(
            self.grid,
            1
        )

    def set_character(self, character):

        print(
            "[VaultTab] Existing layout:",
            self.layout()
        )

        print(
            f"[VaultTab] set_character: "
            f"{getattr(character, 'name', 'UNKNOWN')}"
        )

        print(
            f"[VaultTab] source_file: "
            f"{getattr(character, 'source_file', 'NONE')}"
        )

        # -------------------------------
        # CLEAR GRID CONTENTS
        # -------------------------------
        while self.grid.count():

            item = self.grid.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        # -------------------------------
        # LOAD VAULT DATA FROM STORAGE
        # -------------------------------
        vault = {
            "row1": [],
            "row2": [],
            "row3": [],
        }

        file_path = getattr(
            character,
            "source_file",
            None
        )

        if file_path:

            for line in load_section(
                file_path,
                "Vault"
            ):

                if "=" not in line:
                    continue

                try:

                    key, value = line.split(
                        "=",
                        1
                    )

                    row, col = key.split("_")

                    row_name = (
                        f"row{int(row) + 1}"
                    )

                    if row_name not in vault:
                        continue

                    while (
                        len(vault[row_name])
                        <= int(col)
                    ):
                        vault[row_name].append(
                            None
                        )

                    vault[row_name][int(col)] = value

                except (
                    ValueError,
                    KeyError,
                ) as e:

                    print(
                        f"[VaultTab] Ignoring "
                        f"invalid vault entry: "
                        f"{line} ({e})"
                    )

        print(
            f"[VaultTab] Loaded vault data: "
            f"{vault}"
        )

        # -------------------------------
        # BOX CREATOR
        # -------------------------------
        def create_box(value):

            lbl = QLabel(str(value))

            lbl.setAlignment(
                Qt.AlignCenter
            )

            lbl.setMinimumSize(
                140,
                100
            )

            lbl.setSizePolicy(
                QSizePolicy.Expanding,
                QSizePolicy.Expanding
            )

            lbl.setObjectName(
                "vaultBox"
            )

            return lbl

        # -------------------------------
        # FILL ROW
        # -------------------------------
        def fill_row(
            row_index,
            values,
        ):

            values = values[:3]

            for col in range(3):

                val = (
                    values[col]
                    if (
                        col < len(values)
                        and values[col]
                    )
                    else "-"
                )

                self.grid.addWidget(
                    create_box(val),
                    row_index,
                    col + 1,
                )

        # -------------------------------
        # LABELS
        # -------------------------------
        labels = [
            ("Raid Slots", "row1"),
            ("M+ Slots", "row2"),
            ("Delve Slots", "row3"),
        ]

        for row_index, (
            label_text,
            key,
        ) in enumerate(labels):

            label = QLabel(label_text)

            label.setAlignment(
                Qt.AlignRight
                | Qt.AlignVCenter
            )

            label.setObjectName(
                "vaultRowLabel"
            )

            self.grid.addWidget(
                label,
                row_index,
                0,
            )

            fill_row(
                row_index,
                vault.get(
                    key,
                    [],
                ),
            )

        # -------------------------------
        # GRID STRETCH
        # -------------------------------
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 2)
        self.grid.setColumnStretch(2, 2)
        self.grid.setColumnStretch(3, 2)

        self.grid.setRowStretch(0, 1)
        self.grid.setRowStretch(1, 1)
        self.grid.setRowStretch(2, 1)

        print(
            "[VaultTab] UI rebuild complete"
        )
