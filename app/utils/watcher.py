# File watcher that triggers updates when files change.

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileChangeHandler(FileSystemEventHandler):
  
# Reacts to filesystem changes and calls a callback.
  

    def __init__(self, callback):
        self.callback = callback

    def on_any_event(self, event):
        self.callback()


class FolderWatcher:
  
# Watches a folder for changes using watchdog.
  

    def __init__(self, path, callback):
        self.observer = Observer()
        self.handler = FileChangeHandler(callback)
        self.path = path

    def start(self):
        self.observer.schedule(self.handler, self.path, recursive=False)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()