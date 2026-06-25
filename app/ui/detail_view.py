# Displays detailed information for a single character.

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QTabWidget
)
from PySide6.QtCore import Qt


def format_gold(copper):
    gold = copper // 10000
    silver = (copper % 10000) // 100
    copper_remainder = copper % 100

    parts = []
    if gold > 0:
        parts.append(f"{gold}g")
    if silver > 0:
        parts.append(f"{silver}s")
    if copper_remainder > 0:
        parts.append(f"{copper_remainder}c")

    return " ".join(parts) if parts else "0c"


class DetailView(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

# --------------------------------------------------
# MAIN ENTRY
# --------------------------------------------------

    def set_character(self, character):

# Clear old tabs

        while self.tabs.count():
            widget = self.tabs.widget(0)
            self.tabs.removeTab(0)
            widget.deleteLater()

# -------------------------------
# TAB 1 — OVERVIEW
# -------------------------------

        overview = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"<h2>{character.name}</h2>"))

        info = (
            f"Level {getattr(character, 'level', '-')}, "
            f"{getattr(character, 'race', '-')}, "
            f"{getattr(character, 'character_class', '-')} "
            f"({getattr(character, 'specialization', '-')})"
        )
        layout.addWidget(QLabel(info))

# Gold

        gold = next((c for c in character.currencies if c.name == "Gold"), None)
        if gold:
            layout.addWidget(QLabel(f"<b>Gold:</b> {format_gold(gold.quantity)}"))

# Ascendant currencies

        for c in character.currencies:
            print(c.name, "GROUPS:", c.groups)
            if "Ascendant" in c.name:
                layout.addWidget(QLabel(self._format_currency(c)))

        layout.addStretch()
        overview.setLayout(layout)
        self.tabs.addTab(overview, "Overview")

# -------------------------------
# TAB 2 — CURRENCIES
# -------------------------------
        
        currencies_tab = QWidget()
        currencies_layout = QVBoxLayout()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        content_layout = QVBoxLayout()

        grouped = {}

# Build grouping

        for c in character.currencies:
            groups = getattr(c, "groups", [])

            if not groups:
                grouped.setdefault("Other", []).append(c)
            else:
                for g in groups:
                    grouped.setdefault(g, []).append(c)

# DEBUG - to be removed or deactivated later

        print("DEBUG grouped keys:", list(grouped.keys()))
        print("DEBUG total currencies:", len(character.currencies))

# Render groups

        for group_name in sorted(grouped.keys()):

            title = QLabel(f"<b>{group_name}</b>")   
            title.setTextFormat(Qt.RichText)
            content_layout.addWidget(title)

            for c in sorted(grouped[group_name], key=lambda x: x.name):
                lbl = QLabel(self._format_currency(c))
                content_layout.addWidget(lbl)

        content_layout.addStretch()
        content.setLayout(content_layout)

        scroll.setWidget(content)
        currencies_layout.addWidget(scroll)
        currencies_tab.setLayout(currencies_layout)

        self.tabs.addTab(currencies_tab, "Currencies")


# -------------------------------
# TAB 3 — VAULT
# -------------------------------

        vault_tab = QWidget()
        layout = QVBoxLayout()

        vault = getattr(character, "vault", {
            "row1": [],
            "row2": [],
            "row3": []
        })

        def fmt(values):
            return " | ".join(str(v) for v in values) if values else "-"

        layout.addWidget(QLabel(f"<b>Raid:</b> {fmt(vault.get('row1', []))}"))
        layout.addWidget(QLabel(f"<b>Mythic+:</b> {fmt(vault.get('row2', []))}"))
        layout.addWidget(QLabel(f"<b>Delves:</b> {fmt(vault.get('row3', []))}"))

        layout.addStretch()
        vault_tab.setLayout(layout)
        self.tabs.addTab(vault_tab, "Vault")

# -------------------------------
# TAB 4 — STATS
# -------------------------------

        stats_tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("<b>Primary Attributes</b>"))

        for k, v in getattr(character, "attributes", {}).items():
            layout.addWidget(QLabel(f"{k}: {v}"))

        layout.addWidget(QLabel("<b>Combat Ratings</b>"))

        for k, v in getattr(character, "combat_ratings", {}).items():
            layout.addWidget(QLabel(f"{k}: {v}"))

        layout.addStretch()
        stats_tab.setLayout(layout)
        self.tabs.addTab(stats_tab, "Stats")

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

    def _format_currency(self, currency):
        return (
            f"{currency.name}: {currency.quantity}/{currency.max_total}"
            if getattr(currency, "max_total", None)
            else f"{currency.name}: {currency.quantity}"
        )