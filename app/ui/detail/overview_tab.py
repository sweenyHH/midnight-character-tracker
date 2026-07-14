from PySide6.QtWidgets import (
    QWidget, QLabel, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QVBoxLayout, QHeaderView
)
from .utils import format_gold
from app.ui.detail.notes_widget import NotesWidget
from app.weekly_duties.widget import WeeklyDutiesWidget
from app.ui.detail.vault_progress import VaultProgressWidget

from app.ui.colors import CLASS_COLORS
from app.ui.character_table_helpers import adjust_class_color
from app.utils.logger import logger


class OverviewTab(QWidget):

    def __init__(self):
        super().__init__()

# MAIN LAYOUT (persistent)
        self.layout = QVBoxLayout(self)

# CREATE WIDGETS
        self.notes_widget = NotesWidget()
        self.duties_widget = WeeklyDutiesWidget()
        self.vault_widget = VaultProgressWidget()

# GENERAL INFO LABELS
        self.name_label = QLabel()
        self.info_label = QLabel()
        self.gold_label = QLabel()
        self.other_currencies_label = QLabel()
        self.other_currencies_label.setWordWrap(True)

# PERSISTENT CURRENCY TABLE

        self.currency_table = QTableWidget()

        self.currency_table.setColumnCount(5)
        self.currency_table.setHorizontalHeaderLabels([
            "Currency",
            "Total",
            "Total Max",
            "Weekly",
            "Weekly Max"
        ])

        self.currency_table.setAlternatingRowColors(True)

        header = self.currency_table.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeToContents
        )

        self.currency_table.verticalHeader().setVisible(
            False
        )

# --------------------------------------------------
# PERMANENT LAYOUTS
# --------------------------------------------------

        self.top_row = QHBoxLayout()
        self.bottom_row = QHBoxLayout()

        self.general_widget = QWidget()
        self.general_layout = QVBoxLayout(self.general_widget)

        self.general_layout.addWidget(self.name_label)
        self.general_layout.addWidget(self.info_label)
        self.general_layout.addWidget(self.gold_label)
        self.general_layout.addWidget(
            self.other_currencies_label
        )

        self.left_column = QVBoxLayout()
        self.left_column.addWidget(self.currency_table)
        self.left_column.addWidget(self.vault_widget)

        self.top_row.addWidget(self.general_widget, 2)
        self.top_row.addWidget(self.notes_widget, 3)

        self.bottom_row.addLayout(self.left_column, 2)
        self.bottom_row.addWidget(self.duties_widget, 3)

        self.layout.addLayout(self.top_row)
        self.layout.addLayout(self.bottom_row)



# --------------------------------------------------
    def set_character(self, character):

        logger.info(
            f"OverviewTab set_character: {character.name}"
        )

# ==================================================
# TOP ROW (GENERAL + NOTES)
# ==================================================

        class_name = getattr(
            character,
            "character_class",
            "-"
        )

        self.name_label.setText(
            f"<h2>{character.name}</h2>"
        )

        self.info_label.setText(
            f"<b>Level {getattr(character, 'level', '-')}, </b>"
            f"<b>{getattr(character, 'race', '-')}, </b>"
            f"<b>{class_name} </b>"
            f"<b>({getattr(character, 'specialization', '-')})</b>"
        )

        if class_name in CLASS_COLORS:
            adjusted = adjust_class_color(
                CLASS_COLORS[class_name]
            )

            self.info_label.setStyleSheet(
                f"color: {adjusted};"
            )
        else:
            self.info_label.setStyleSheet("")

        gold = next(
            (
                x for x in character.currencies
                if x.name == "Gold"
            ),
            None
        )

        if gold:
            self.gold_label.setText(
                f"<b>Gold:</b> "
                f"{format_gold(gold.quantity)}"
            )
        else:
            self.gold_label.setText("")

        other_currencies = [
            c for c in character.currencies
            if getattr(c, "groups", None)
            and "Other" in c.groups
            and c.name != "Gold"
        ]

        combined = {}

        for currency in other_currencies:
            combined.setdefault(
                currency.name,
                0
            )

            combined[currency.name] += (
                currency.quantity or 0
            )

        if combined:

            lines = []

            for name in sorted(combined):
                lines.append(
                    f"<b>{name}:</b> "
                    f"{combined[name]}"
                )

            self.other_currencies_label.setText(
                "<br>".join(lines)
            )

        else:
            self.other_currencies_label.setText("")


# REUSE WIDGET
        self.notes_widget.set_character(character)

# ==================================================
# BOTTOM ROW (CURRENCIES + DUTIES)
# ==================================================

# -------------------------------
# LEFT COLUMN (CURRENCIES + VAULT)
# -------------------------------

        currencies = [
            c for c in character.currencies
            if c.weekly_max is not None
        ]

        logger.info(
            f"OverviewTab created currency table with "
            f"{len(currencies)} rows for {character.name}"
        )

        self.currency_table.clearContents()
        self.currency_table.setRowCount(len(currencies))

        for row, c in enumerate(currencies):
            self.currency_table.setItem(row, 0, QTableWidgetItem(c.name))
            self.currency_table.setItem(row, 1, QTableWidgetItem(str(c.quantity) if c.quantity else "-"))
            self.currency_table.setItem(row, 2, QTableWidgetItem(str(c.max_total) if c.max_total else "-"))
            self.currency_table.setItem(row, 3, QTableWidgetItem(str(c.weekly_current) if c.weekly_current else "-"))
            self.currency_table.setItem(row, 4, QTableWidgetItem(str(c.weekly_max) if c.weekly_max else "-"))


# REUSE VAULT WIDGET
        self.vault_widget.set_character(character)

# REUSE DUTIES WIDGET
        self.duties_widget.set_character(character)

