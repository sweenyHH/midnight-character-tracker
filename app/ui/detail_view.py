from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from .detail.overview_tab import OverviewTab
from .detail.currencies_tab import CurrenciesTab
from .detail.vault_tab import VaultTab
from .detail.stats_tab import StatsTab
from .detail.reputation_tab import ReputationTab
from .detail.debug_tab import DebugTab


class DetailView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

# instantiate tabs
        self.overview_tab = OverviewTab()
        self.currencies_tab = CurrenciesTab()
        self.vault_tab = VaultTab()
        self.stats_tab = StatsTab()
        self.reputation_tab = ReputationTab()
        self.debug_tab = DebugTab()

        self.tabs.addTab(self.overview_tab, "Overview")
        self.tabs.addTab(self.currencies_tab, "Currencies")
        self.tabs.addTab(self.vault_tab, "Vault")
        self.tabs.addTab(self.stats_tab, "Stats")
        self.tabs.addTab(self.reputation_tab, "Reputation")
        self.tabs.addTab(self.debug_tab, "Debug")

    def set_character(self, character):
        self.overview_tab.set_character(character)
        self.currencies_tab.set_character(character)
        self.vault_tab.set_character(character)
        self.stats_tab.set_character(character)
        self.reputation_tab.set_character(character)
        self.debug_tab.set_character(character)