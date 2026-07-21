from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
)
from PySide6.QtCore import Qt

from app.localization.ui_strings import get_ui_string
from app.ui.detail.currencies.currency_group_widget import CurrencyGroupWidget
from app.ui.detail.currencies.currency_constants import GROUP_ORDER


class CurrenciesTab(QWidget):

    def __init__(self):
        super().__init__()

        self.group_widgets = {}

        root_layout = QVBoxLayout(self)

        # ==========================================
        # CONTROL BUTTONS
        # ==========================================

        self.btn_widget = QWidget()
        self.btn_widget.setMaximumHeight(40)

        btn_layout = QHBoxLayout(self.btn_widget)
        btn_layout.setContentsMargins(0, 0, 0, 0)

        self.expand_btn = QPushButton(get_ui_string("expand_all"))
        self.collapse_btn = QPushButton(get_ui_string("collapse_all"))

        self.expand_btn.clicked.connect(self.expand_all)
        self.collapse_btn.clicked.connect(self.collapse_all)

        btn_layout.addWidget(self.expand_btn)
        btn_layout.addWidget(self.collapse_btn)
        btn_layout.addStretch()

        root_layout.addWidget(self.btn_widget)

        # ==========================================
        # SCROLL AREA
        # ==========================================

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        root_layout.addWidget(self.scroll)

        # ==========================================
        # CONTENT CONTAINER
        # ==========================================

        self.container = QWidget()

        self.main_layout = QHBoxLayout(self.container)

        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.left_layout.setSpacing(8)
        self.right_layout.setSpacing(8)

        self.left_layout.setAlignment(Qt.AlignTop)
        self.right_layout.setAlignment(Qt.AlignTop)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 1)

        self.scroll.setWidget(self.container)

        # ==========================================
        # BUILD GROUP WIDGETS ONCE
        # ==========================================

        mid = len(GROUP_ORDER) // 2
        left_groups = GROUP_ORDER[:mid]
        right_groups = GROUP_ORDER[mid:]

        for group_name in left_groups:

            widget = CurrencyGroupWidget(group_name)
            self.group_widgets[group_name] = widget
            self.left_layout.addWidget(widget)

        for group_name in right_groups:

            widget = CurrencyGroupWidget(group_name)
            self.group_widgets[group_name] = widget
            self.right_layout.addWidget(widget)

    def set_character(self, character):

        grouped = {}

        for currency in character.currencies:

            if (currency.currency_key == "gold"):
                continue

            groups = getattr(currency, "groups", None)

            if not groups:

                grouped.setdefault("Other", [],).append(currency)

            else:

                for group in groups:

                    group = (group or "Other")
                    grouped.setdefault(group, []).append(currency)

        for group_name in GROUP_ORDER:

            currencies = grouped.get(group_name, [])

            self.group_widgets[group_name].set_currencies(currencies)

    def expand_all(self):

        for widget in (self.group_widgets.values()):

            widget.expand()

    def collapse_all(self):

        for widget in (self.group_widgets.values()):

            widget.collapse()


