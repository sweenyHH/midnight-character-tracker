# Handles loading and managing data from the filesystem.

import os
from app.parser.txt_parser import parse_txt


class DataService:

# Central service responsible for loading character data from files.

    def __init__(self):
        self.folder_path = None

# Stores parsed character objects

        self.characters = []

# Track file modification times to detect updates

        self.file_timestamps = {}

    def set_folder(self, path):

# Sets the directory where character files are located.

        self.folder_path = path

# Reset everything when switching folder

        self.characters = []
        self.file_timestamps = {}

        self.load_data()

    def load_data(self):

# Loads all character files from the selected directory.
# Detects new and updated files.

        if not self.folder_path:
            return

        print("[DataService] Scanning folder...")

# Temporary list to rebuild character list

        updated_characters = []

        for file in os.listdir(self.folder_path):

# Only process .txt files

            if not file.endswith(".txt"):
                continue

            full_path = os.path.join(self.folder_path, file)

            try:
# Get last modified time

                last_modified = os.path.getmtime(full_path)

# Check if file is new or updated

                if (full_path not in self.file_timestamps or
                        self.file_timestamps[full_path] != last_modified):

                    status = "NEW" if full_path not in self.file_timestamps else "UPDATED"
                    print(f"[DataService] {status} file: {file}")

# Parse file

                    character = parse_txt(full_path)

# Store updated timestamp

                    self.file_timestamps[full_path] = last_modified

                else:
# File unchanged → reuse existing character

                    character = self._get_existing_character(full_path)

                if character:
                    updated_characters.append(character)

            except Exception as e:
                print(f"[DataService] Error processing {file}: {e}")

# Replace character list

        self.characters = updated_characters

    def _get_existing_character(self, file_path):

# Returns already loaded character for unchanged file.

        for character in self.characters:
            if getattr(character, "source_file", None) == file_path:
                return character

        return None

    def get_characters(self):

# Returns all loaded characters.

        return self.characters
