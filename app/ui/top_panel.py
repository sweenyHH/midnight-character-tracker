from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QGridLayout,
    QFrame,
)

from PySide6.QtCore import Qt, Signal

from app.ui.settings_dialog import SettingsDialog
from app.ui.detail.utils import format_gold
from app.utils.number_formatter import format_number


from app.game_data.currency_catalog import (
    get_currency_by_key,
)


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
    def update_reputation(self, reputation_list, currency_totals=None):

        if currency_totals is None:
            currency_totals = {}

# Clear previous content
        while self.rep_layout.count():

            item = self.rep_layout.takeAt(0)

            if item.widget():

                item.widget().deleteLater()

            elif item.layout():

                while item.layout().count():

                    child = item.layout().takeAt(0)

                    if child.widget():
                        child.widget().deleteLater()    

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

        renown.sort(key=lambda r: r.name)


        def chunk(lst, size=3):
            return [
                lst[i:i + size]
                for i in range(0, len(lst), size)
            ]

        renown_chunks = chunk(renown)

        main_row = QHBoxLayout()


# -------------------------------
# RENOWN BLOCK
# -------------------------------
        renown_widget = QFrame()
        
        renown_widget.setObjectName(
            "topPanelFrame"
        )
        renown_widget.setFrameShape(
            QFrame.Box
        )

        renown_layout = QVBoxLayout(renown_widget)
        renown_layout.setAlignment(Qt.AlignTop)

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
# WARBAND RESOURCES BLOCK
# -------------------------------

        currency_widget = QFrame()
        currency_widget.setObjectName(
            "topPanelFrame"
        )

        currency_widget.setFrameShape(
            QFrame.Box
        )

        currency_layout = QVBoxLayout(
            currency_widget
        )
        currency_layout.setAlignment(Qt.AlignTop)

        currency_title = QLabel(
            "<b>Warband Resources</b>"
        )

        currency_title.setAlignment(
            Qt.AlignCenter
        )

        currency_layout.addWidget(
            currency_title
        )

        currency_grid = QGridLayout()

        CURRENCY_COLUMNS = [
            [
                "gold",
                "brimming_arcana",
                "remnant_of_anguish",
                "voidlight_marl",
            ],
            [
                "angler_pearls",
                "undercoin",
                "timewarped_badge",
                "community_coupons",
            ],
            [
                "conquest",
                "honor",
                "bloody_token",
            ],
        ]

        currency_definitions = {
            key: get_currency_by_key(key)
            for group in CURRENCY_COLUMNS
            for key in group
        }

        for group_index, group in enumerate(
            CURRENCY_COLUMNS
        ):

            col_offset = group_index * 2

            for row, key in enumerate(group):

                definition = currency_definitions[key]

                currency_grid.addWidget(
                    QLabel(f"<b>{definition.english_name}</b>"),
                    row,
                    col_offset
                )

                value = currency_totals.get(
                    key,
                    0
                )

                if key == "gold"
                    value_text = format_gold(value)
                else:
                    value_text = format_number(value)

                currency_grid.addWidget(
                    QLabel(value_text),
                    row,
                    col_offset + 1
                )

        currency_layout.addLayout(
            currency_grid
        )
        
# -------------------------------
# FINAL LAYOUT
# -------------------------------
        main_row.addWidget(
            renown_widget
        )

        main_row.addWidget(
            currency_widget
        )

        main_row.setStretch(0, 2)
        main_row.setStretch(1, 3)

        self.rep_layout.addLayout(
            main_row
        )
