# File watcher that triggers updates when files change.

import threading

from app.utils.logger import logger

# polling observer (required for WSL)
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler
from app.services.internal_write_guard import write_guard



class FileChangeHandler(FileSystemEventHandler):

# Reacts to filesystem changes and calls a callback.

    def __init__(self, callback):
        self.callback = callback

# Timer for debounce logic

        self.timer = None

# Delay in seconds (adjust if needed)

        self.delay = 1.0

    def on_any_event(self, event):

# Ignore directory events

        if event.is_directory:
            return

# Only react to .txt files

        if not event.src_path.endswith(".txt"):
            return

        logger.info(
          f"Watcher detected change: "
           f"{event.src_path}"
        )

# Ignore application-owned writes

        if write_guard.is_internal_write(
            event.src_path
        ):
            logger.info(
                f"Ignoring internal write: "
                f"{event.src_path}"
            )
            return

# Cancel previous timer if still running

        if self.timer:

            logger.info(
                "Watcher debounce timer reset"
            )

            self.timer.cancel()

# Start new timer (debounce)

        self.timer = threading.Timer(self.delay, self._trigger_callback)
        self.timer.start()

    def _trigger_callback(self):

        logger.info(
            "Watcher callback triggered"
        )

# Call the UI update callback

        self.callback()


class FolderWatcher:

# Watches a folder for changes using watchdog.

    def __init__(self, path, callback):
        self.observer = Observer()
        self.handler = FileChangeHandler(callback)
        self.path = path

    def start(self):

        print(f"[FolderWatcher] Watching {self.path}...")

        logger.info(
            f"Started watching folder: "
            f"{self.path}"
        )

        self.observer.schedule(self.handler, self.path, recursive=False)
        self.observer.start()

    def stop(self):

        print("[FolderWatcher] Stopping...")

        logger.info(
            "Folder watcher stopped"
        )

        self.observer.stop()
        self.observer.join()