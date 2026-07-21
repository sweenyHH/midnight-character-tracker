from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from app.ui.colors import ITEM_QUALITY_COLORS
from app.localization.ui_strings import get_ui_string
from app.services.display_language import get_display_language
from app.game_data.equipment_slot_catalog import get_equipment_slot_display_name


class EquipmentWidget(QWidget):

    def _set_table_height(self, table, extra_padding=8):

        row_count = table.rowCount()
        header_height = (table.horizontalHeader().height())
        row_height = (table.verticalHeader().defaultSectionSize())
        total = (header_height + (row_height * row_count))
        table.setMinimumHeight(total + extra_padding)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel(
                f"<b>{get_ui_string('equipment')}</b>"
            )
        )

        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            [
                get_ui_string("slot"),
                get_ui_string("name"),
                get_ui_string("item_level"),
                get_ui_string("type"),
                get_ui_string("enchanted"),
            ]
        )

        layout.addWidget(self.table)

    def set_character(self, character):

        equipment = getattr(character, "equipment", [])

        equipment = [
            item
            for item in equipment
            if item.slot not in (
                "shirt",
                "tabard",
            )
        ]

        self.table.setRowCount(len(equipment))
        language = (get_display_language())

        for row, item in enumerate(equipment):

            slot_name = (
                get_equipment_slot_display_name(
                    item.slot,
                    language,
                )
            )

            slot_item = (QTableWidgetItem(slot_name))

            font = slot_item.font()
            font.setBold(True)
            slot_item.setFont(font)
            slot_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            self.table.setItem(row, 0, slot_item)

            name_item = (QTableWidgetItem(item.name))
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            quality = getattr(item, "quality", None)

            if quality:
                quality = quality.lower()

            if item.name == "Empty":

                name_item.setForeground(QColor("#888888"))

            elif (quality in ITEM_QUALITY_COLORS):

                name_item.setForeground(
                    QColor(
                        ITEM_QUALITY_COLORS[
                            quality
                        ]
                    )
                )

                if quality in ("epic", "legendary"):

                    font = (name_item.font())
                    font.setBold(True)
                    name_item.setFont(font)

            self.table.setItem(row, 1, name_item)

            ilvl = (
                str(item.item_level)
                if item.item_level
                is not None
                else "-"
            )

            self.table.setItem(row, 2, QTableWidgetItem(ilvl))

            item_type = (
                item.item_type
                if item.item_type
                else "-"
            )

            self.table.setItem(row, 3, QTableWidgetItem(item_type))

            enchanted = (
                get_ui_string("yes")
                if item.enchanted
                else get_ui_string("no")
            )

            ench_item = (QTableWidgetItem(enchanted))
            ench_item.setTextAlignment(Qt.AlignCenter)

            if item.enchanted:

                ench_item.setForeground(QColor("#4caf50"))

            self.table.setItem(row, 4, ench_item)

        header = (self.table.horizontalHeader())

        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.table.verticalHeader().setDefaultSectionSize(30)
        self._set_table_height(self.table)