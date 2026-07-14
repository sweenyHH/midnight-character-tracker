# Centralizes application refresh and reload logic.
#
# Responsibilities:
# - Reload coordination
# - Reload protection
# - Watcher integration
# - Selection preservation
# - Refresh notifications
#
# The service remains UI-agnostic.

from PySide6.QtCore import QObject, Signal

from app.utils.logger import logger
from app.utils.watcher import FolderWatcher
from app.services.warband_currency_service import (
    get_warband_currency_totals
)


class RefreshResult:
    """
    Holds all data produced by a refresh operation.

    This object is returned by RefreshService and
    consumed by the UI layer.
    """

    def __init__(
        self,
        characters,
        reputations,
        currency_totals,
        selected_character,
    ):
        self.characters = characters
        self.reputations = reputations
        self.currency_totals = currency_totals
        self.selected_character = (
            selected_character
        )


class RefreshService(QObject):
    """
    Coordinates application refresh operations.
    """

    refresh_requested = Signal()

    def __init__(self, data_service):
        super().__init__()

        # Service responsible for loading character data.
        self.data_service = data_service

        # Prevent concurrent refresh operations.
        self._reload_running = False

        logger.info(
            "RefreshService initialized"
        )

    def _find_refreshed_character(
        self,
        characters,
        selected_character,
    ):
        """
        Returns the freshly loaded character instance
        matching the previously selected character.
        """

        if selected_character is None:
            return None

        selected_source_file = (
            selected_character.source_file
        )

        for character in characters:
            if (
                character.source_file
                == selected_source_file
            ):
                return character

        return None

    def refresh_data(
        self,
        selected_character=None,
    ):
        """
        Reloads character data and returns
        all information required by the UI.
        """

        logger.info(
            "Refreshing application data"
        )

        self.data_service.load_data()

        characters = (
            self.data_service.get_characters()
        )

        currency_totals = (
            get_warband_currency_totals(
                characters
            )
        )

        reputations = (
            self.data_service.get_top_reputations()
        )

        refreshed_character = (
            self._find_refreshed_character(
                characters,
                selected_character,
            )
        )

        return RefreshResult(
            characters=characters,
            reputations=reputations,
            currency_totals=currency_totals,
            selected_character=refreshed_character,
        )

    def execute_refresh(
        self,
        selected_character=None,
    ):
        """
        Executes a protected refresh operation.

        Prevents overlapping refresh execution and
        returns a RefreshResult when successful.
        """

        if self._reload_running:
            logger.warning(
                "Refresh skipped - already running"
            )
            return None

        self._reload_running = True

        try:
            return self.refresh_data(
                selected_character
            )
        finally:
            self._reload_running = False

    def start_watcher(self, folder):
        """
        Starts filesystem monitoring.
        """

        self.watcher = FolderWatcher(
            folder,
            self._handle_file_change,
        )

        self.watcher.start()

    def stop_watcher(self):
        """
        Stops filesystem monitoring.
        """

        if hasattr(self, "watcher"):
            self.watcher.stop()

    def _handle_file_change(self):
        """
        Called when the import folder changes.
        """

        logger.info(
            "RefreshService detected file change"
        )

        self.refresh_requested.emit()