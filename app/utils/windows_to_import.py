import time
import shutil
import os

# Use PollingObserver (required for WSL + Windows filesystem)
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler


SOURCE_DIR = "/mnt/d/Games/WoWCharExports/"
TARGET_DIR = "/home/malte/workspace/bootdotdev/midnightchartracker/import/"


class TxtHandler(FileSystemEventHandler):

    def __init__(self):
        super().__init__()

# Track last modification timestamp of processed files

        self.file_timestamps = {}

    def is_file_stable(self, path, wait_time=1.0):
        """
        Checks if file size is stable over short time → ensures file finished writing.
        """
        try:
            size1 = os.path.getsize(path)
            time.sleep(wait_time)
            size2 = os.path.getsize(path)

            return size1 == size2
        except Exception:
            return False

    def process(self, src_path):

# Only process .txt files

        if not src_path.endswith(".txt"):
            return

        try:
# Get last modified time of source file

            last_modified = os.path.getmtime(src_path)

        except Exception as e:
            print(f"[SKIP] Could not read file: {src_path} ({e})")
            return

# Skip if file unchanged

        if (src_path in self.file_timestamps and
                self.file_timestamps[src_path] == last_modified):
            return

# Wait until file is stable (important for WoW exports)

        if not self.is_file_stable(src_path):
            print(f"[SKIP] File still being written: {src_path}")
            return

        filename = os.path.basename(src_path)
        target_path = os.path.join(TARGET_DIR, filename)

        action = "Copying"

# Detect if this is an update of an existing file

        if src_path in self.file_timestamps:
            action = "Updating"

        print(f"{action}: {src_path} -> {target_path}")

        try:

# Copy and overwrite existing file if present

            shutil.copy2(src_path, target_path)

# Update timestamp AFTER successful operation

            self.file_timestamps[src_path] = last_modified

        except Exception as e:
            print(f"Error copying file: {e}")

    def on_created(self, event):

# Debug output to verify events

        print(f"[DEBUG] Created event: {event.src_path}")

# Ignore directories

        if not event.is_directory:
            self.process(event.src_path)

    def on_modified(self, event):

# Debug output to verify events

        print(f"[DEBUG] Modified event: {event.src_path}")

# Ignore directories

        if not event.is_directory:
            self.process(event.src_path)


class WindowsToImportWatcher:

    def __init__(self):

# Observer initialized only if source directory is valid

        self.observer = None
        self.handler = TxtHandler()

    def start(self):

# Check if Windows source directory exists (important for non-WSL systems)

        if not os.path.exists(SOURCE_DIR):
            print("[WindowsToImportWatcher] Source folder not found -> watcher disabled")
            return

# Check if target directory exists (prevents copy errors)

        if not os.path.exists(TARGET_DIR):
            print("[WindowsToImportWatcher] Target folder not found -> watcher disabled")
            return

# Initialize observer only when both directories are valid

        self.observer = Observer()

# Schedule watcher on Windows folder

        self.observer.schedule(self.handler, SOURCE_DIR, recursive=False)
        self.observer.start()

        print(f"[WindowsToImportWatcher] Watching {SOURCE_DIR}...")

    def stop(self):

# Only stop observer if it was started

        if self.observer:
            print("[WindowsToImportWatcher] Stopping...")

            self.observer.stop()
            self.observer.join()