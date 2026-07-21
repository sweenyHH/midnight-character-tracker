from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from .detail.tracking_tab import TrackingTab

from app.ui.detail.stats.stats_tab import StatsTab
from .detail.reputation_tab import ReputationTab

from app.ui.detail.overview.overview_tab import OverviewTab
from app.utils.logger import logger
from app.localization.ui_strings import get_ui_string
from app.ui.detail.currencies.currencies_tab import CurrenciesTab


class DetailView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

# instantiate tabs
        self.overview_tab = OverviewTab()
        self.tracking_tab = TrackingTab()
        self.currencies_tab = CurrenciesTab()

        self.stats_tab = StatsTab()
        self.reputation_tab = ReputationTab()


        self.tracking_tab.vault_widget.on_save_callback = (self.refresh_vault_tab)

        self.current_character = None

        self.tabs.addTab(
            self.overview_tab,
            get_ui_string("overview"),
        )

        self.tabs.addTab(
            self.tracking_tab,
            get_ui_string("tracking"),
        )

        self.tabs.addTab(
            self.currencies_tab,
            get_ui_string("currencies"),
        )

        self.tabs.addTab(
            self.stats_tab,
            get_ui_string("stats"),
        )

        self.tabs.addTab(
            self.reputation_tab,
            get_ui_string("reputation"),
        )

    def set_character(self, character):

        self.current_character = character

        logger.info(
            f"DetailView loading character: "
            f"{character.name}"
        )

        logger.info("Updating OverviewTab")
        self.overview_tab.set_character(character)

        logger.info("Updating TrackingTab")
        self.tracking_tab.set_character(character)

        logger.info("Updating CurrenciesTab")
        self.currencies_tab.set_character(character)

        logger.info("Updating StatsTab")
        self.stats_tab.set_character(character)

        logger.info("Updating ReputationTab")
        self.reputation_tab.set_character(character)

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