from app.utils.logger import logger
from app.utils.app_paths import get_data_dir

SETTINGS_FILE = get_data_dir() / "settings.txt"

logger.info(
    f"Settings file: {SETTINGS_FILE}"
)

def load_setting(key, default=None):

    if not SETTINGS_FILE.exists():
        return default

    with open(SETTINGS_FILE, encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if "=" not in line:
                continue

            k, v = line.split("=", 1)

            if k == key:
                return v

    return default


def save_setting(key, value):

    settings = {}

    if SETTINGS_FILE.exists():

        with open(SETTINGS_FILE, encoding="utf-8") as f:

            for line in f:

                line = line.strip()

                if "=" not in line:
                    continue

                k, v = line.split("=", 1)

                settings[k] = v

    settings[key] = str(value)

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:

        for k in sorted(settings):
            f.write(f"{k}={settings[k]}\n")