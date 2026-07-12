import logging
from logging.handlers import RotatingFileHandler

from app.utils.app_paths import get_log_dir


# --------------------------------------------------
# LOG DIRECTORY
# --------------------------------------------------

LOG_DIR = get_log_dir()

LOG_FILE = LOG_DIR / "mct.log"


# --------------------------------------------------
# LOGGER
# --------------------------------------------------

logger = logging.getLogger("mct")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers
if not logger.handlers:

    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)