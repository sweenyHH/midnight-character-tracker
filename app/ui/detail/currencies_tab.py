from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QScrollArea, QSizePolicy
)

from PySide6.QtCore import Qt

from .utils import get_layout


# --------------------------------------------------
# GROUP ORDER (custom domain order)
# --------------------------------------------------

GROUP_ORDER = [

    "Midnight",
    "War Within",
    "Shadowlands",
    "Legion",
    "Mists of Pandaria",
    "Wrath of the Lich King",
    "Player vs. Player",

    "Season 1",
    "Dragonflight", 
    "Battle for Azeroth",
    "Warlords of Draenor",
    "Cataclysm",
    "Burning Crusade",
    "Miscellaneous",
    "Other"
]


# --------------------------------------------------
# GROUP WIDGET (collapsible section)
# --------------------------------------------------

class CurrencyGroupWidget(QWidget):

    def __init__(self, group_name, currencies):
        super().__init__()

        self.group_name = group_name
        self.currencies = currencies
        self.is_expanded = False

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

# HEADER
        self.header = QPushButton(f"▶ {group_name}")
        self.header.setCheckable(True)
        self.header.clicked.connect(self.toggle)

        self.layout.addWidget(self.header)

# TABLE     
        self.table = QTableWidget()
        self.table.hide()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._build_table()

        self.layout.addWidget(self.table)

# -------------------------
# BUILD TABLE
# -------------------------
    def _build_table(self):
        table = self.table

        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Name", "Amount", "Max"])
        table.setRowCount(len(self.currencies))

        table.verticalHeader().setVisible(False)

        
        for row, c in enumerate(self.currencies):

# NAME (BOLD)
            name_item = QTableWidgetItem(c.name)
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
        row_count = self.table.rowCount()

        if row_count == 0:
            self.table.setMinimumHeight(50)
            return

        header_height = self.table.horizontalHeader().height()
        row_height = self.table.verticalHeader().defaultSectionSize()

        total_height = header_height + (row_count * row_height) + 5

        self.table.setMinimumHeight(total_height)

# -------------------------
# TOGGLE
# -------------------------
    def toggle(self):
        self.is_expanded = not self.is_expanded

        if self.is_expanded:
            self._adjust_table_height()

        self.table.setVisible(self.is_expanded)

        arrow = "▼" if self.is_expanded else "▶"
        self.header.setText(f"{arrow} {self.group_name}")

    def expand(self):
        if not self.is_expanded:
            self.toggle()

    def collapse(self):
        if self.is_expanded:
            self.toggle()


# --------------------------------------------------
# MAIN TAB
# --------------------------------------------------

class CurrenciesTab(QWidget):

    def set_character(self, character):
        layout = get_layout(self)

        self.group_widgets = []

# GROUP CURRENCIES
        grouped = {}

        for c in character.currencies:
            if c.name == "Gold":
                continue

            groups = getattr(c, "groups", None)

            if not groups:
                grouped.setdefault("Other", []).append(c)
            else:
                for g in groups:
                    g = g or "Other"
                    grouped.setdefault(g, []).append(c)

        grouped = {k: v for k, v in grouped.items() if v}



# SORT GROUPS
        def sort_groups(grouped):
            ordered = [g for g in GROUP_ORDER if g in grouped]
            remaining = sorted(g for g in grouped if g not in GROUP_ORDER)
            return ordered + remaining

        ordered_groups = sort_groups(grouped)

# SPLIT
        mid = len(ordered_groups) // 2
        left_groups = ordered_groups[:mid]
        right_groups = ordered_groups[mid:]

# CONTROL BUTTONS
        btn_layout = QHBoxLayout()

        expand_btn = QPushButton("Expand All")
        collapse_btn = QPushButton("Collapse All")

        expand_btn.clicked.connect(self.expand_all)
        collapse_btn.clicked.connect(self.collapse_all)

        btn_layout.addWidget(expand_btn)
        btn_layout.addWidget(collapse_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)

# SCROLL AREA
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        main_layout = QHBoxLayout(container)

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        left_layout.setSpacing(8)
        right_layout.setSpacing(8)

        left_layout.setAlignment(Qt.AlignTop)
        right_layout.setAlignment(Qt.AlignTop)

# LEFT COLUMN
        left_first = True

        for group_name in left_groups:
            widget = CurrencyGroupWidget(group_name, grouped[group_name])
            self.group_widgets.append(widget)

            if left_first:
                widget.toggle()
                left_first = False

            left_layout.addWidget(widget)

# RIGHT COLUMN
        right_first = True

        for group_name in right_groups:
            widget = CurrencyGroupWidget(group_name, grouped[group_name])
            self.group_widgets.append(widget)

            if right_first:
                widget.toggle()
                right_first = False

            right_layout.addWidget(widget)

# ADD LAYOUTS
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 1)

        scroll.setWidget(container)
        layout.addWidget(scroll)

# CONTROL METHODS 
    def expand_all(self):
        for widget in self.group_widgets:
            widget.expand()

    def collapse_all(self):
        for widget in self.group_widgets:
            widget.collapse()


