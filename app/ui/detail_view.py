from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from .detail.overview_tab import OverviewTab
from .detail.currencies_tab import CurrenciesTab
from .detail.vault_tab import VaultTab
from .detail.stats_tab import StatsTab
from .detail.reputation_tab import ReputationTab
from .detail.debug_tab import DebugTab
from app.utils.logger import logger


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

        self.overview_tab.vault_widget.on_save_callback = (self.refresh_vault_tab)

        self.current_character = None

        self.tabs.addTab(self.overview_tab, "Overview")
        self.tabs.addTab(self.currencies_tab, "Currencies")
        self.tabs.addTab(self.vault_tab, "Vault")
        self.tabs.addTab(self.stats_tab, "Stats")
        self.tabs.addTab(self.reputation_tab, "Reputation")
        self.tabs.addTab(self.debug_tab, "Debug")

    def set_character(self, character):

        self.current_character = character

        logger.info(
            f"DetailView loading character: "
            f"{character.name}"
        )

        logger.info("Updating OverviewTab")
        self.overview_tab.set_character(character)

        logger.info("Updating CurrenciesTab")
        self.currencies_tab.set_character(character)

        logger.info("Updating VaultTab")
        self.vault_tab.set_character(character)

        logger.info("Updating StatsTab")
        self.stats_tab.set_character(character)

        logger.info("Updating ReputationTab")
        self.reputation_tab.set_character(character)

        logger.info("Updating DebugTab")
        self.debug_tab.set_character(character)

        logger.info(
            f"DetailView finished loading: "
            f"{character.name}"
        )

    def refresh_vault_tab(self):

        if self.current_character is None:
            return

        self.vault_tab.set_character(
            self.current_character
        )