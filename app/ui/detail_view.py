# Displays detailed information for a single character.

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget,
    QTableWidget, QTableWidgetItem
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

        self.setObjectName("detailView")

        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tabs.setObjectName("detailTabs")

        self.layout.addWidget(self.tabs)

        self._create_tabs()

    # --------------------------------------------------
    # TAB SETUP
    # --------------------------------------------------

    def _create_tabs(self):
        self.overview_tab = QWidget()
        self.currencies_tab = QWidget()
        self.vault_tab = QWidget()
        self.stats_tab = QWidget()
        self.reputation_tab = QWidget()
        self.debug_tab = QWidget()

        self.tabs.addTab(self.overview_tab, "Overview")
        self.tabs.addTab(self.currencies_tab, "Currencies")
        self.tabs.addTab(self.vault_tab, "Vault")
        self.tabs.addTab(self.stats_tab, "Stats")
        self.tabs.addTab(self.reputation_tab, "Reputation")
        self.tabs.addTab(self.debug_tab, "Debug")

    # --------------------------------------------------
    # MAIN ENTRY
    # --------------------------------------------------

    def set_character(self, character):
        self.character = character

        self._update_overview()
        self._update_currencies()
        self._update_vault()
        self._update_stats()
        self._update_reputation()
        self._update_debug()

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------

    def _clear_layout(self, widget):
        if widget.layout():
            while widget.layout().count():
                item = widget.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

        
    def _get_layout(self, widget):
        layout = widget.layout()

        if layout is None:
            layout = QVBoxLayout()
            widget.setLayout(layout)
        else:
            self._clear_layout(widget)

        return layout


    # --------------------------------------------------
    # OVERVIEW
    # --------------------------------------------------

    def _update_overview(self):
        layout = self._get_layout(self.overview_tab)

        c = self.character

        layout.addWidget(QLabel(f"<h2>{c.name}</h2>"))

        info = (
            f"Level {getattr(c, 'level', '-')}, "
            f"{getattr(c, 'race', '-')}, "
            f"{getattr(c, 'character_class', '-')} "
            f"({getattr(c, 'specialization', '-')})"
        )
        layout.addWidget(QLabel(info))

        # Gold (special handling)
        gold = next((x for x in c.currencies if x.name == "Gold"), None)
        if gold:
            layout.addWidget(QLabel(f"<b>Gold:</b> {format_gold(gold.quantity)}"))

        layout.addStretch()

    # --------------------------------------------------
    # CURRENCIES (FLAT TABLE)
    # --------------------------------------------------

    def _update_currencies(self):
        layout = self._get_layout(self.currencies_tab)

        table = QTableWidget()
        table.setObjectName("currencyTable")

        currencies = [
            c for c in self.character.currencies if c.name != "Gold"
        ]

        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Name", "Amount", "Max", "Group"])
        table.setRowCount(len(currencies))

        for row, c in enumerate(currencies):
            table.setItem(row, 0, QTableWidgetItem(c.name))
            table.setItem(row, 1, QTableWidgetItem(str(c.quantity)))

            max_val = getattr(c, "max_total", "")
            table.setItem(row, 2, QTableWidgetItem(str(max_val)))

            groups = ", ".join(getattr(c, "groups", [])) or "Other"
            table.setItem(row, 3, QTableWidgetItem(groups))

        table.resizeColumnsToContents()
        layout.addWidget(table)

    # --------------------------------------------------
    # VAULT
    # --------------------------------------------------

    def _update_vault(self):
        layout = self._get_layout(self.vault_tab)

        vault = getattr(self.character, "vault", {
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

    # --------------------------------------------------
    # STATS (TABLES)
    # --------------------------------------------------



    def _update_stats(self):
        layout = self._get_layout(self.stats_tab)

        # Create horizontal container
        container = QWidget()
        h_layout = QHBoxLayout(container)

        c = self.character

        # -------------------------
        # LEFT: Attributes
        # -------------------------

        attr_widget = QWidget()
        attr_layout = QVBoxLayout(attr_widget)

        attr_layout.addWidget(QLabel("<b>Primary Attributes</b>"))

        attr_table = QTableWidget()
        attr_table.setColumnCount(2)
        attr_table.setHorizontalHeaderLabels(["Attribute", "Value"])

        attrs = getattr(c, "attributes", {})
        attr_table.setRowCount(len(attrs))

        for row, (k, v) in enumerate(attrs.items()):
            attr_table.setItem(row, 0, QTableWidgetItem(k))
            attr_table.setItem(row, 1, QTableWidgetItem(str(v)))

        attr_table.resizeColumnsToContents()

        attr_layout.addWidget(attr_table)

        # -------------------------
        # RIGHT: Combat Ratings
        # -------------------------

        combat_widget = QWidget()
        combat_layout = QVBoxLayout(combat_widget)

        combat_layout.addWidget(QLabel("<b>Combat Ratings</b>"))

        combat_table = QTableWidget()
        combat_table.setColumnCount(2)
        combat_table.setHorizontalHeaderLabels(["Stat", "Value"])

        combat = getattr(c, "combat_ratings", {})
        combat_table.setRowCount(len(combat))

    
        for row, (k, v) in enumerate(combat.items()):

            rating = v.get("rating", "-") if isinstance(v, dict) else "-"
            percent = v.get("percent", "-") if isinstance(v, dict) else "-"

            if percent != "-":
                percent = f"{percent}%"

            combat_table.setItem(row, 0, QTableWidgetItem(k))
            combat_table.setItem(row, 1, QTableWidgetItem(str(rating)))
            combat_table.setItem(row, 2, QTableWidgetItem(str(percent)))


        
        combat_table.resizeColumnsToContents()  
        combat_layout.addWidget(combat_table)

        # -------------------------
        # ADD TO HORIZONTAL LAYOUT
        # -------------------------

        h_layout.addWidget(attr_widget)
        h_layout.addWidget(combat_widget)

        # Optional: equal width
        h_layout.setStretch(0, 1)
        h_layout.setStretch(1, 1)

        layout.addWidget(container)

    # --------------------------------------------------
    # REPUTATION (INTENTIONALLY EMPTY)
    # --------------------------------------------------

    def _update_reputation(self):
        layout = self._get_layout(self.reputation_tab)

        layout.addWidget(QLabel(
            "Character-specific reputation will appear here in a future update."
        ))

        layout.addStretch()

    # --------------------------------------------------
    # DEBUG
    # --------------------------------------------------

    def _update_debug(self):
        layout = self._get_layout(self.debug_tab)

        c = self.character

        layout.addWidget(QLabel(f"Source file: {getattr(c, 'source_file', '-')}"))
        layout.addWidget(QLabel(f"Currencies: {len(c.currencies)}"))
        layout.addWidget(QLabel(f"Attributes: {len(getattr(c, 'attributes', {}))}"))
        layout.addWidget(QLabel(f"Combat stats: {len(getattr(c, 'combat_ratings', {}))}"))

        layout.addStretch()