from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


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

    def format_vault_values(self, values):
        if not values:
            return ""
        return " | ".join(str(v) for v in values)

    def get_attr(self, char, attr_name):
        value = getattr(char, attr_name, None)
        return str(value) if value is not None else "-"

    def get_currency_value(self, char, name):
        for c in char.currencies:
            if c.name == name:
                return c
        return None

    def load_characters(self, characters):

        self.setRowCount(len(characters))

        for row, char in enumerate(characters):

# Name

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

# Basic info

            self.setItem(row, 1, QTableWidgetItem(self.get_attr(char, "character_class")))
            self.setItem(row, 2, QTableWidgetItem(self.get_attr(char, "avg_item_level")))
            self.setItem(row, 3, QTableWidgetItem(self.get_attr(char, "level")))
            self.setItem(row, 4, QTableWidgetItem(self.get_attr(char, "specialization")))

# Vault

            vault = getattr(char, "vault", {"row1": [], "row2": [], "row3": []})

            self.setItem(row, 7, QTableWidgetItem(self.format_vault_values(vault.get("row1", []))))
            self.setItem(row, 8, QTableWidgetItem(self.format_vault_values(vault.get("row2", []))))
            self.setItem(row, 9, QTableWidgetItem(self.format_vault_values(vault.get("row3", []))))

# Coffer Keys

            coffer = self.get_currency_value(char, "Restored Coffer Key")
            self.setItem(row, 5, QTableWidgetItem(str(coffer.quantity) if coffer else "0"))

# Spark

            spark = self.get_currency_value(char, "Radiant Spark Dust")
            if spark:
                value = f"{spark.quantity}/{spark.max_total}" if spark.max_total else str(spark.quantity)
            else:
                value = "-"

            self.setItem(row, 6, QTableWidgetItem(value))

        self.resizeColumnsToContents()