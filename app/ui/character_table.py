from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from app.ui.colors import CLASS_COLORS

from .character_table_helpers import (
    NumericItem,
    format_vault_values,
    get_attr,
    get_currency_value,
    adjust_class_color,
)

from app.storage.vault_storage import load_user_vault


class CharacterTable(QTableWidget):

    def __init__(self):
        super().__init__()

        self.setColumnCount(10)
        self.setHorizontalHeaderLabels([
            "Character",
            "Class",
            "Item Level",
            "Level",
            "Specialization",
            "Coffer Keys",
            "R. Spark Dust",
            "Raid",
            "Mystic+",
            "Delves"
        ])

        self.setSortingEnabled(True)

# --------------------------------------------------

    def load_characters(self, characters):

        self.setSortingEnabled(False)

        self.clearContents()
        self.setRowCount(len(characters))

        for row, char in enumerate(characters):

# -------------------------------
# Name
# -------------------------------
            name_item = QTableWidgetItem(char.name)
            name_item.setData(Qt.UserRole, char)

            if char.faction == "Alliance":
                name_item.setForeground(QColor("#4aa3ff"))
            elif char.faction == "Horde":
                name_item.setForeground(QColor("#ff4a4a"))

            font = name_item.font()
            font.setBold(True)
            name_item.setFont(font)

            self.setItem(row, 0, name_item)

# -------------------------------
# Class
# -------------------------------
            class_name = get_attr(char, "character_class")

            class_item = QTableWidgetItem(class_name)

            if class_name in CLASS_COLORS:
                adjusted = adjust_class_color(CLASS_COLORS[class_name])
                class_item.setForeground(QColor(adjusted))

            self.setItem(row, 1, class_item)

# -------------------------------
# Item Level
# -------------------------------
            ilvl_raw = getattr(char, "avg_item_level", None)

            try:
                ilvl_value = int(ilvl_raw)
            except (TypeError, ValueError):
                ilvl_value = 0

            ilvl_item = NumericItem(
                str(ilvl_raw) if ilvl_raw is not None else "-",
                ilvl_value
            )

            self.setItem(row, 2, ilvl_item)

# -------------------------------
# Level / Specialization
# -------------------------------
            self.setItem(
                row,
                3,
                QTableWidgetItem(get_attr(char, "level"))
            )

            self.setItem(
                row,
                4,
                QTableWidgetItem(get_attr(char, "specialization"))
            )

# -------------------------------
# Vault
# -------------------------------
            vault = load_user_vault(char)

            def has_value(values):
                return any(v for v in values if str(v).strip())

            raid_values = vault.get("row1", [])
            mplus_values = vault.get("row2", [])
            delve_values = vault.get("row3", [])

            raid_sort = 1 if has_value(raid_values) else 0
            mplus_sort = 1 if has_value(mplus_values) else 0
            delve_sort = 1 if has_value(delve_values) else 0

            raid_item = NumericItem(
                format_vault_values(raid_values),
                raid_sort
            )

            mplus_item = NumericItem(
                format_vault_values(mplus_values),
                mplus_sort
            )

            delve_item = NumericItem(
                format_vault_values(delve_values),
                delve_sort
            )

            self.setItem(row, 7, raid_item)
            self.setItem(row, 8, mplus_item)
            self.setItem(row, 9, delve_item)

# -------------------------------
# Coffer Keys
# -------------------------------
            coffer = get_currency_value(
                char,
                "Restored Coffer Key"
            )

            coffer_value = coffer.quantity if coffer else 0

            coffer_item = NumericItem(
                str(coffer_value),
                coffer_value
            )

            self.setItem(row, 5, coffer_item)

# -------------------------------
# Spark Dust
# -------------------------------
            spark = get_currency_value(
                char,
                "Radiant Spark Dust"
            )

            if spark:
                value = (
                    f"{spark.quantity}/{spark.max_total}"
                    if spark.max_total
                    else str(spark.quantity)
                )
                sort_value = spark.quantity
            else:
                value = "-"
                sort_value = 0

            spark_item = NumericItem(
                value,
                sort_value
            )

            self.setItem(row, 6, spark_item)

        self.resizeColumnsToContents()
        self.setSortingEnabled(True)