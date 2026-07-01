from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from .utils import get_layout

from app.ui.colors import ITEM_QUALITY_COLORS


class StatsTab(QWidget):

    
    def _set_table_height(self, table):
        row_count = table.rowCount()

        header_height = table.horizontalHeader().height()

# use sizeHint for accurate row height
        row_height = table.verticalHeader().defaultSectionSize()

        total = header_height + (row_height * row_count)

        table.setMinimumHeight(total + 4)

    def set_character(self, character):
        layout = get_layout(self)

        container = QWidget()
        main_layout = QHBoxLayout(container)

# ==================================================
# LEFT SIDE (Attributes + Combat stacked)
# ==================================================
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

# -------------------------------
# ATTRIBUTES
# -------------------------------
        attr_table = QTableWidget()
        attr_table.setColumnCount(2)
        attr_table.setHorizontalHeaderLabels(["Attribute", "Value"])

        attrs = getattr(character, "attributes", {})
        attr_table.setRowCount(len(attrs))

        for row, (k, v) in enumerate(attrs.items()):
            attr_table.setItem(row, 0, QTableWidgetItem(k))
            attr_table.setItem(row, 1, QTableWidgetItem(str(v)))

        attr_table.resizeColumnsToContents()
        attr_table.resizeRowsToContents()

        attr_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self._set_table_height(attr_table)

        attr_box = QVBoxLayout()
        attr_container = QWidget()
        attr_container.setLayout(attr_box)
        attr_box.addWidget(QLabel("<b>Primary Attributes</b>"))
        attr_box.addWidget(attr_table)

# -------------------------------
# COMBAT RATINGS
# -------------------------------
        combat_table = QTableWidget()
        combat_table.setColumnCount(3)
        combat_table.setHorizontalHeaderLabels(["Stat", "Rating", "%"])

        combat = getattr(character, "combat_ratings", {})
        combat_table.setRowCount(len(combat))

        for row, (k, v) in enumerate(combat.items()):
            rating = v.get("rating", "-")
            percent = v.get("percent", "-")
            percent = f"{percent}%" if percent != "-" else "-"

            combat_table.setItem(row, 0, QTableWidgetItem(k))
            combat_table.setItem(row, 1, QTableWidgetItem(str(rating)))
            combat_table.setItem(row, 2, QTableWidgetItem(str(percent)))

        combat_table.resizeColumnsToContents()
        combat_table.resizeRowsToContents()

        combat_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self._set_table_height(combat_table)

        combat_box = QVBoxLayout()
        combat_container = QWidget()
        combat_container.setLayout(combat_box)
        combat_box.addWidget(QLabel("<b>Combat Ratings</b>"))
        combat_box.addWidget(combat_table)

        left_layout.addWidget(attr_container)
        left_layout.addWidget(combat_container)
        left_layout.setAlignment(Qt.AlignTop)

# ==================================================
# RIGHT SIDE (Equipment)
# ==================================================
        equipment_widget = QWidget()
        equipment_layout = QVBoxLayout(equipment_widget)

        equipment_layout.addWidget(QLabel("<b>Equipment</b>"))

        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([
            "Slot",
            "Name",
            "Item Level",
            "Type",
            "Enchanted"
        ])

        equipment = getattr(character, "equipment", [])
        table.setRowCount(len(equipment))

        for row, item in enumerate(equipment):

# Slot
            slot_item = QTableWidgetItem(item.slot)
            slot_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            table.setItem(row, 0, slot_item)

# NAME + COLOR
            name_item = QTableWidgetItem(item.name)
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            quality = getattr(item, "quality", None)
            if quality:
                quality = quality.lower()

            if item.name == "Empty":
                name_item.setForeground(QColor("#888888"))

            elif quality in ITEM_QUALITY_COLORS:
                name_item.setForeground(QColor(ITEM_QUALITY_COLORS[quality]))

                if quality in ("epic", "legendary"):
                    font = name_item.font()
                    font.setBold(True)
                    name_item.setFont(font)

            table.setItem(row, 1, name_item)

# Item Level
            ilvl = str(item.item_level) if item.item_level is not None else "-"
            table.setItem(row, 2, QTableWidgetItem(ilvl))

# Type
            item_type = item.item_type if item.item_type else "-"
            table.setItem(row, 3, QTableWidgetItem(item_type))

# Enchanted
            enchanted = "Yes" if item.enchanted else "No"
            ench_item = QTableWidgetItem(enchanted)
            ench_item.setTextAlignment(Qt.AlignCenter)

            if item.enchanted:
                ench_item.setForeground(QColor("#4caf50"))

            table.setItem(row, 4, ench_item)

        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        table.resizeRowsToContents()

# ensure all 18 rows visible
        self._set_table_height(table)

        equipment_layout.addWidget(table)

# ==================================================
# ADD TO MAIN LAYOUT
# ==================================================
        main_layout.addWidget(left_widget)
        main_layout.addWidget(equipment_widget)

        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 1)

        layout.addWidget(container)