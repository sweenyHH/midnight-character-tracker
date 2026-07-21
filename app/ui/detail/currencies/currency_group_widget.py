from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtCore import Qt

from app.game_data.currency_catalog import get_currency_display_name
from app.services.display_language import get_display_language
from app.localization.ui_strings import get_ui_string
from app.ui.detail.currencies.currency_constants import get_group_display_name


class CurrencyGroupWidget(QWidget):

    def __init__(self, group_name):
        super().__init__()

        self.group_name = group_name
        self.currencies = []


        self.is_expanded = False
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

# HEADER

        display_name = (get_group_display_name(group_name))

        self.header = QPushButton(f"▶ {display_name}")
        self.header.setCheckable(True)
        self.header.clicked.connect(self.toggle)
        self.layout.addWidget(self.header)

# TABLE

        self.table = QTableWidget()
        self.table.hide()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._build_table()
        self.layout.addWidget(self.table)


    def set_currencies(
        self,
        currencies,
    ):
        self.currencies = currencies

        self.table.clearContents()

        self.table.setRowCount(
            len(currencies)
        )

        self._build_table()        

# -------------------------
# BUILD TABLE
# -------------------------

    def _build_table(self):

        table = self.table
        if table.columnCount() == 0:

            table.setColumnCount(3)

            table.setHorizontalHeaderLabels(
                [
                    get_ui_string("name"),
                    get_ui_string("amount"),
                    get_ui_string("max"),
                ]
            )

        table.setRowCount(
            len(self.currencies)
        )

        table.verticalHeader().setVisible(False)

        for row, c in enumerate(self.currencies):

            language = (get_display_language())

            display_name = (
                get_currency_display_name(
                    c.currency_key,
                    language,
                )
                or c.name
            )

# NAME (BOLD)

            name_item = (QTableWidgetItem(display_name))
            font = name_item.font()
            font.setBold(True)
            name_item.setFont(font)
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            table.setItem(row, 0, name_item)

# Amount

            table.setItem(row, 1, QTableWidgetItem(str(c.quantity)))

# Max

            max_val = getattr(c, "max_total", "")

            table.setItem(row, 2, QTableWidgetItem(str(max_val)))

        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)

        self._adjust_table_height()

# -------------------------
# AUTO HEIGHT
# -------------------------

    def _adjust_table_height(self):

        row_count = (self.table.rowCount())

        if row_count == 0:
            self.table.setMinimumHeight(50)
            return

        header_height = (self.table.horizontalHeader().height())

        row_height = (self.table.verticalHeader().defaultSectionSize())

        total_height = (header_height + (row_count * row_height) + 5)

        self.table.setMinimumHeight(total_height)

# -------------------------
# TOGGLE
# -------------------------

    def toggle(self):

        self.is_expanded = (not self.is_expanded)

        if self.is_expanded:
            self._adjust_table_height()

        self.table.setVisible(self.is_expanded)

        arrow = (
            "▼"
            if self.is_expanded
            else "▶"
        )
        self.header.setText(
            f"{arrow} "
            f"{get_group_display_name(self.group_name)}"
        )

    def expand(self):

        if not self.is_expanded:
            self.toggle()

    def collapse(self):

        if self.is_expanded:
            self.toggle()