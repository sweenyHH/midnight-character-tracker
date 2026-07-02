from PySide6.QtWidgets import (
    QWidget, QLabel, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QVBoxLayout, QHeaderView
)
from PySide6.QtCore import Qt

from .utils import format_gold
from app.ui.detail.notes_widget import NotesWidget
from app.weekly_duties.widget import WeeklyDutiesWidget
from app.ui.detail.vault_progress import VaultProgressWidget

from app.ui.colors import CLASS_COLORS
from app.ui.character_table_helpers import adjust_class_color


class OverviewTab(QWidget):

    def __init__(self):
        super().__init__()

# MAIN LAYOUT (persistent)
        self.layout = QVBoxLayout(self)

# CREATE WIDGETS
        self.notes_widget = NotesWidget()
        self.duties_widget = WeeklyDutiesWidget()
        self.vault_widget = VaultProgressWidget()

# --------------------------------------------------
    def set_character(self, character):


# FULL LAYOUT CLEAR
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                item.layout().deleteLater()

# ==================================================
# TOP ROW (GENERAL + NOTES)
# ==================================================
        top_row = QHBoxLayout()

# LEFT — GENERAL
        general_widget = QWidget()
        general_layout = QVBoxLayout(general_widget)

        general_layout.addWidget(QLabel(f"<h2>{character.name}</h2>"))

        class_name = getattr(character, "character_class", "-")

        info_label = QLabel(
            f"<b>Level {getattr(character, 'level', '-')}, </b>"
            f"<b>{getattr(character, 'race', '-')}, </b>"
            f"<b>{class_name} </b>"
            f"<b>({getattr(character, 'specialization', '-')})</b>"
        )

        if class_name in CLASS_COLORS:
            adjusted = adjust_class_color(CLASS_COLORS[class_name])
            info_label.setStyleSheet(f"color: {adjusted};")


        general_layout.addWidget(info_label)

        gold = next((x for x in character.currencies if x.name == "Gold"), None)
        if gold:
            general_layout.addWidget(QLabel(f"<b>Gold:</b> {format_gold(gold.quantity)}"))


# OTHER CURRENCIES
        other_currencies = [
            c for c in character.currencies
            if getattr(c, "groups", None)
            and "Other" in c.groups
            and c.name != "Gold"
        ]

        for currency in sorted(other_currencies, key=lambda x: x.name):
            general_layout.addWidget(
                QLabel(
                    f"<b>{currency.name}:</b> {currency.quantity}"
                )
            )

            

        general_layout.addStretch()

# REUSE WIDGET
        self.notes_widget.set_character(character)

        top_row.addWidget(general_widget)
        top_row.addWidget(self.notes_widget)
        top_row.setStretch(0, 1)
        top_row.setStretch(1, 1)

        self.layout.addLayout(top_row)

# ==================================================
# BOTTOM ROW (CURRENCIES + DUTIES)
# ==================================================
        bottom_row = QHBoxLayout()

# -------------------------------
# LEFT COLUMN (CURRENCIES + VAULT)
# -------------------------------
        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)

        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([
            "Currency",
            "Total",
            "Total Max",
            "Weekly",
            "Weekly Max"
        ])

        table.setAlternatingRowColors(True)

        currencies = [
            c for c in character.currencies
            if c.weekly_max is not None
        ]

        table.setRowCount(len(currencies))

        for row, c in enumerate(currencies):
            table.setItem(row, 0, QTableWidgetItem(c.name))
            table.setItem(row, 1, QTableWidgetItem(str(c.quantity) if c.quantity else "-"))
            table.setItem(row, 2, QTableWidgetItem(str(c.max_total) if c.max_total else "-"))
            table.setItem(row, 3, QTableWidgetItem(str(c.weekly_current) if c.weekly_current else "-"))
            table.setItem(row, 4, QTableWidgetItem(str(c.weekly_max) if c.weekly_max else "-"))

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        table.verticalHeader().setVisible(False)

        left_layout.addWidget(table)

# REUSE VAULT WIDGET
        self.vault_widget.set_character(character)
        left_layout.addWidget(self.vault_widget)

# REUSE DUTIES WIDGET
        self.duties_widget.set_character(character)

        bottom_row.addWidget(left_column)
        bottom_row.addWidget(self.duties_widget)

        bottom_row.setStretch(0, 1)
        bottom_row.setStretch(1, 1)

        self.layout.addLayout(bottom_row)

        self.layout.addStretch()
