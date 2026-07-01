from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt


class ReputationTab(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

# -------------------------------
# SEARCH FIELD
# -------------------------------
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search reputations (min 3 letters)...")
        self.search.textChanged.connect(self.apply_filter)

        self.layout.addWidget(self.search)

# -------------------------------
# TABLE
# -------------------------------
        self.table = QTableWidget()

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([
            "Faction",
            "Level",
            "Progress"
        ])

        self.table.setSortingEnabled(True)

# COLUMN RESIZE CONFIG 
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Faction
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Level
        header.setSectionResizeMode(2, QHeaderView.Stretch)           # Progress 

        self.layout.addWidget(self.table)

        self.reputations = []

# -------------------------------
# LOAD CHARACTER
# -------------------------------
    def set_character(self, character):
        self.reputations = sorted(
            character.reputations,
            key=lambda r: r.name.lower()
        )
        self.populate_table(self.reputations)

# -------------------------------
# POPULATE TABLE
# -------------------------------
    def populate_table(self, rep_list):

        self.table.setRowCount(len(rep_list))

        for row, rep in enumerate(rep_list):

# -------------------------------
# FACTION (LEFT)
# -------------------------------
            name_item = QTableWidgetItem(rep.name)
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row, 0, name_item)

# -------------------------------
# LEVEL (CENTER)
# -------------------------------
            if rep.rep_type == "renown":
                level_text = f"Renown {rep.level}"
            else:
                level_text = str(rep.level) if rep.level else "-"

            level_item = QTableWidgetItem(level_text)
            level_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, level_item)

# -------------------------------
# PROGRESS (LEFT)
# -------------------------------
            if rep.current is not None and rep.maximum is not None:
                progress_text = f"{rep.current} / {rep.maximum}"
            else:
                progress_text = "-"

            progress_item = QTableWidgetItem(progress_text)
            progress_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.table.setItem(row, 2, progress_item)

    # -------------------------------
    # FILTER
    # -------------------------------
    def apply_filter(self, text):

        text = text.strip().lower()

        if len(text) < 3:
            self.populate_table(self.reputations)
            return

        filtered = [
            rep for rep in self.reputations
            if text in rep.name.lower()
        ]

        self.populate_table(filtered)

