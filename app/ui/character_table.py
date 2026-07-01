from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import os
from app.ui.colors import CLASS_COLORS


class NumericItem(QTableWidgetItem):
    def __init__(self, display_value, sort_value):
        super().__init__(display_value)
        self.sort_value = sort_value

    def __lt__(self, other):
        if isinstance(other, NumericItem):
            return self.sort_value < other.sort_value
        return super().__lt__(other)


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
        return " | ".join(str(v) for v in values if v)

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
# Basic info
# -------------------------------

            class_name = self.get_attr(char, "character_class")

            class_item = QTableWidgetItem(class_name)

# APPLY CLASS COLOR
            from app.ui.colors import CLASS_COLORS

            if class_name in CLASS_COLORS:
                class_item.setForeground(QColor(CLASS_COLORS[class_name]))

            self.setItem(row, 1, class_item)



            self.setItem(row, 3, QTableWidgetItem(self.get_attr(char, "level")))
            self.setItem(row, 4, QTableWidgetItem(self.get_attr(char, "specialization")))

            
            ilvl_raw = getattr(char, "avg_item_level", None)

# convert safely to int for sorting
            try:
                ilvl_value = int(ilvl_raw)
            except:
                ilvl_value = 0

            ilvl_item = NumericItem(str(ilvl_raw) if ilvl_raw is not None else "-", ilvl_value)

            self.setItem(row, 2, ilvl_item)


# ==================================================
# LOAD USER VAULT DATA
# ==================================================
            vault = getattr(char, "vault", {"row1": [], "row2": [], "row3": []})

            user_vault = {"row1": [], "row2": [], "row3": []}
            file_path = getattr(char, "source_file", None)

            if file_path and os.path.exists(file_path):

                in_user_block = False
                in_vault = False

                with open(file_path, encoding="utf-8") as f:
                    for line in f:
                        stripped = line.strip()

                        if stripped == "### USER_DATA_START ###":
                            in_user_block = True
                            continue

                        if stripped == "### USER_DATA_END ###":
                            break

                        if in_user_block and stripped == "Vault:":
                            in_vault = True
                            continue

                        if in_vault:
                            if "=" in stripped:
                                key, value = stripped.split("=")

                                row_idx, col_idx = key.split("_")
                                row_name = f"row{int(row_idx) + 1}"

                                while len(user_vault[row_name]) <= int(col_idx):
                                    user_vault[row_name].append(None)

                                user_vault[row_name][int(col_idx)] = value

                            elif stripped.endswith(":"):
                                break

            if any(user_vault[r] for r in user_vault):
                vault = user_vault

# -------------------------------
# Vault display + BOOLEAN SORT
# -------------------------------
            def has_value(values):
                return any(v for v in values if str(v).strip())

            raid_values = vault.get("row1", [])
            mplus_values = vault.get("row2", [])
            delve_values = vault.get("row3", [])

            raid_sort = 1 if has_value(raid_values) else 0
            mplus_sort = 1 if has_value(mplus_values) else 0
            delve_sort = 1 if has_value(delve_values) else 0

            raid_item = NumericItem(self.format_vault_values(raid_values), raid_sort)
            mplus_item = NumericItem(self.format_vault_values(mplus_values), mplus_sort)
            delve_item = NumericItem(self.format_vault_values(delve_values), delve_sort)

            self.setItem(row, 7, raid_item)
            self.setItem(row, 8, mplus_item)
            self.setItem(row, 9, delve_item)

# -------------------------------
# Coffer Keys
# -------------------------------
            coffer = self.get_currency_value(char, "Restored Coffer Key")
            coffer_value = coffer.quantity if coffer else 0

            coffer_item = NumericItem(str(coffer_value), coffer_value)
            self.setItem(row, 5, coffer_item)

# -------------------------------
# Spark
# -------------------------------
            spark = self.get_currency_value(char, "Radiant Spark Dust")

            if spark:
                value = f"{spark.quantity}/{spark.max_total}" if spark.max_total else str(spark.quantity)
                sort_value = spark.quantity
            else:
                value = "-"
                sort_value = 0

            spark_item = NumericItem(value, sort_value)
            self.setItem(row, 6, spark_item)

        self.resizeColumnsToContents()