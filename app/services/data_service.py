# Handles loading and managing data from the filesystem.

import os
from app.parser.base_parser import parse_txt

# Central service responsible for loading character data from files.

class DataService:

    def __init__(self):
        self.folder_path = None

# Stores parsed character objects

        self.characters = []

# Stores latest reputation data (shared across characters)

        self.reputation_data = []

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

        updated_characters = []

        for file in os.listdir(self.folder_path):

# Only process .txt files

            if not file.endswith(".txt"):
                continue

            full_path = os.path.join(self.folder_path, file)

            try:
                last_modified = os.path.getmtime(full_path)

# Check if file is new or updated

                if (
                    full_path not in self.file_timestamps
                    or self.file_timestamps[full_path] != last_modified
                ):

                    status = (
                        "NEW"
                        if full_path not in self.file_timestamps
                        else "UPDATED"
                    )
                    print(f"[DataService] {status} file: {file}")

# Parser returns only character

                    character = parse_txt(full_path)

# Reputations as attribute of character

                    if hasattr(character, "reputations") and character.reputations:
                        self.reputation_data = character.reputations

# Store updated timestamp
                    
                    self.file_timestamps[full_path] = last_modified


                else:
                    character = self._get_existing_character(full_path)

# Re-parse if missing
                    if character is None:
                        character = parse_txt(full_path)


                if character:
                    updated_characters.append(character)

                    print("DEBUG Character:", character.name)
                    print("DEBUG currencies:", len(character.currencies))

            except Exception as e:
                print(f"[DataService] Error processing {file}: {e}")

# Replace character list

        self.characters = updated_characters

# Returns already loaded character for unchanged file.

    def _get_existing_character(self, file_path):

        for character in self.characters:
            if getattr(character, "source_file", None) == file_path:
                return character

        return None

# Returns all loaded characters.

    def get_characters(self):

        return self.characters

# Returns latest reputation data

    def get_reputation(self):

        return self.reputation_data

