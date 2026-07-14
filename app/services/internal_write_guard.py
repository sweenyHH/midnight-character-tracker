from pathlib import Path
import time


class InternalWriteGuard:
    """
    Tracks files recently modified by the application.

    The folder watcher can use this information to
    ignore file system events caused by user data saves.
    """

    def __init__(self):
        self._writes = {}

    def register_write(self, file_path):
        """
        Marks a file as recently written by the app.
        """

        self._writes[
            str(Path(file_path).resolve())
        ] = time.time()

    def is_internal_write(
        self,
        file_path,
        max_age=2.0,
    ):
        """
        Returns True if the file was recently written
        by the application.
        """

        file_path = str(
            Path(file_path).resolve()
        )

        timestamp = self._writes.get(
            file_path
        )

        if timestamp is None:
            return False

        age = time.time() - timestamp

        if age > max_age:
            del self._writes[file_path]
            return False

        return True


write_guard = InternalWriteGuard()