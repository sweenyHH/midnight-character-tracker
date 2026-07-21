from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSizePolicy,
)

from app.localization.ui_strings import get_ui_string
from app.services.display_language import get_display_language
from app.game_data.combat_rating_catalog import get_combat_rating_display_name


class CombatRatingsWidget(QWidget):

    def _set_table_height(self, table, extra_padding=8):
        
        row_count = table.rowCount()
        header_height = (table.horizontalHeader().height())
        row_height = (table.verticalHeader().defaultSectionSize())
        total = (header_height + (row_height * row_count))
        table.setMinimumHeight(total + extra_padding)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"<b>{get_ui_string('combat_ratings')}</b>"))

        self.combat_table = QTableWidget()
        self.combat_table.verticalHeader().setVisible(False)
        self.combat_table.setColumnCount(3)
        self.combat_table.setHorizontalHeaderLabels(
            [
                get_ui_string("stat"),
                get_ui_string("rating"),
                "%",
            ]
        )

        layout.addWidget(self.combat_table)

    def set_character(self, character):

        combat = getattr(
            character,
            "combat_ratings",
            {},
        )

        self.combat_table.setRowCount(len(combat))

        language = (get_display_language())

        for row, (k, v) in enumerate(combat.items()):

            rating = v.get("rating", "-")

            percent = v.get("percent", "-")

            percent = (
                f"{percent}%"
                if percent != "-"
                else "-"
            )

            display_name = (
                get_combat_rating_display_name(
                    k,
                    language,
                )
            )

            stat_item = (
                QTableWidgetItem(
                    display_name
                )
            )

            font = stat_item.font()

            font.setBold(True)

            stat_item.setFont(font)

            self.combat_table.setItem(
                row,
                0,
                stat_item,
            )

            self.combat_table.setItem(
                row,
                1,
                QTableWidgetItem(
                    str(rating)
                ),
            )

            self.combat_table.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(percent)
                ),
            )

        self.combat_table.verticalHeader().setDefaultSectionSize(30)

        self.combat_table.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed,
        )

        self._set_table_height(
            self.combat_table,
            extra_padding=12,
        )

        self.combat_table.setMaximumHeight(self.combat_table.minimumHeight())

        header = (self.combat_table.horizontalHeader())
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)