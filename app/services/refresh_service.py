# Centralizes application refresh and reload logic.
#
# This service will gradually become responsible for:
# - Reload coordination
# - Reload protection
# - Watcher integration
# - Selection preservation
# - Refresh notifications
#
# The service remains UI-agnostic.


from app.utils.logger import logger

class RefreshService:
    """
    Coordinates application refresh operations.

    This is currently a skeleton implementation and
    will be expanded incrementally during the reload
    architecture refactor.
    """

    def __init__(self):
        # Prevent concurrent refresh operations.
        self._reload_running = False

        logger.info(
            "RefreshService initialized"
        )

    def is_reload_running(self):
        return self._reload_running

    def start_reload(self):

        self._reload_running = True

    def finish_reload(self):

        self._reload_running = False