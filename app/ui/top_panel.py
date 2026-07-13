from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QGridLayout,
)
from PySide6.QtCore import Qt

from PySide6.QtCore import Qt, Signal

from app.ui.settings_dialog import SettingsDialog


class TopPanel(QWidget):

    settings_changed = Signal()

    def __init__(self, paste_cb, back_cb, warband_cb):
        super().__init__()

        main_layout = QVBoxLayout(self)

# --------------------------------------------------
# ROW 1 — BUTTONS
# --------------------------------------------------
        button_row = QHBoxLayout()

        self.paste_btn = QPushButton("Paste Character Data")
        self.paste_btn.clicked.connect(paste_cb)

        self.warband_btn = QPushButton("Warband Tasks")
        self.warband_btn.clicked.connect(warband_cb)

        self.settings_btn = QPushButton("Settings")
        self.settings_btn.clicked.connect(
            self.open_settings
        )

        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(back_cb)
        self.back_btn.hide()

        button_row.addWidget(self.paste_btn)
        button_row.addWidget(self.warband_btn)
        button_row.addWidget(self.settings_btn)
        button_row.addWidget(self.back_btn)

        button_row.addStretch()

        main_layout.addLayout(button_row)

# --------------------------------------------------
# ROW 2 — REPUTATION
# --------------------------------------------------
        self.rep_container = QWidget()
        self.rep_layout = QVBoxLayout(self.rep_container)

        main_layout.addWidget(self.rep_container)

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

    def open_settings(self):

        dialog = SettingsDialog(self)

        dialog.settings_saved.connect(
            self.settings_changed.emit
        )

        dialog.exec()

# --------------------------------------------------
# UPDATE METHOD
# --------------------------------------------------
    def update_reputation(self, reputation_list):

# Clear previous content
        while self.rep_layout.count():
            item = self.rep_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        if not reputation_list:
            self.rep_layout.addWidget(
                QLabel("No reputation data available")
            )
            return

# Split
        renown = [
            r for r in reputation_list
            if r.rep_type == "renown"
        ]

        normal = [
            r for r in reputation_list
            if r.rep_type != "renown"
        ]

        renown.sort(key=lambda r: r.name)
        normal.sort(key=lambda r: r.name)

        def chunk(lst, size=3):
            return [
                lst[i:i + size]
                for i in range(0, len(lst), size)
            ]

        renown_chunks = chunk(renown)
        normal_chunks = chunk(normal)

        main_row = QHBoxLayout()

# -------------------------------
# RENOWN BLOCK
# -------------------------------
        renown_widget = QWidget()
        renown_layout = QVBoxLayout(renown_widget)

        renown_title = QLabel("<b>Renown</b>")
        renown_title.setAlignment(Qt.AlignCenter)

        renown_layout.addWidget(renown_title)

        renown_grid = QGridLayout()

        def add_group(grid, group, col_offset):

            for row, rep in enumerate(group):

                name = QLabel(
                    f"<b>{rep.name}</b>"
                )

                grid.addWidget(
                    name,
                    row,
                    col_offset
                )

                grid.addWidget(
                    QLabel(str(rep.level)),
                    row,
                    col_offset + 1
                )

        for i, group in enumerate(
            renown_chunks[:2]
        ):
            add_group(
                renown_grid,
                group,
                i * 2
            )

        renown_layout.addLayout(
            renown_grid
        )

# -------------------------------
# STANDARD BLOCK
# -------------------------------
        normal_widget = QWidget()
        normal_layout = QVBoxLayout(
            normal_widget
        )

        normal_title = QLabel(
            "<b>Standard</b>"
        )

        normal_title.setAlignment(
            Qt.AlignCenter
        )

        normal_layout.addWidget(
            normal_title
        )

        normal_grid = QGridLayout()

        def add_standard(
            grid,
            group,
            col_offset
        ):

            for row, rep in enumerate(group):

                name = QLabel(
                    f"<b>{rep.name}</b>"
                )

                if (
                    rep.current
                    and rep.maximum
                ):
                    value = QLabel(
                        f"{rep.level} "
                        f"({rep.current}/{rep.maximum})"
                    )
                else:
                    value = QLabel(
                        str(rep.level)
                    )

                grid.addWidget(
                    name,
                    row,
                    col_offset
                )

                grid.addWidget(
                    value,
                    row,
                    col_offset + 1
                )

        for i, group in enumerate(
            normal_chunks[:2]
        ):
            add_standard(
                normal_grid,
                group,
                i * 2
            )

        normal_layout.addLayout(
            normal_grid
        )

# -------------------------------
# FINAL LAYOUT
# -------------------------------
        main_row.addWidget(
            renown_widget
        )

        main_row.addWidget(
            normal_widget
        )

        main_row.setStretch(0, 1)
        main_row.setStretch(1, 1)

        self.rep_layout.addLayout(
            main_row
        )