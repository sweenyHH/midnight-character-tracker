# Handles loading and managing data from the filesystem.

import os
from app.parser.base_parser import parse_txt
from app.game_data.reputations import FEATURED_REPUTATIONS

from app.utils.logger import logger

class DataService:

    def __init__(self):
        self.folder_path = None

# Stores parsed character objects
        self.characters = []

# Stores latest reputation data (shared across characters)
        self.reputation_data = []

# Track file modification times to detect updates
        self.file_timestamps = {}

# --------------------------------------------------
# SET FOLDER
# --------------------------------------------------
    def set_folder(self, path):

        self.folder_path = path

        logger.info(
            f"Data folder set to: {path}"
        )

# Reset everything when switching folder
        self.characters = []
        self.file_timestamps = {}

        self.load_data()

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
    def load_data(self):

        if not self.folder_path:
            return

        logger.info(
            "Scanning data folder"
        )



        updated_characters = []

        for file in os.listdir(self.folder_path):

            if not file.endswith(".txt"):
                continue

            full_path = os.path.join(self.folder_path, file)

            try:
                last_modified = os.path.getmtime(full_path)

# NEW or UPDATED file
                if (
                    full_path not in self.file_timestamps
                    or self.file_timestamps[full_path] != last_modified
                ):

                    status = (
                        "NEW"
                        if full_path not in self.file_timestamps
                        else "UPDATED"
                    )

                    logger.info(
                     f"{status} character file: {file}"
                    )


                    character = parse_txt(full_path)

                    logger.info(
                        f"Parsed character: "
                        f"{character.name}"
                    )

# store reputations (latest snapshot)
                    if hasattr(character, "reputations") and character.reputations:
                        self.reputation_data = character.reputations

                    self.file_timestamps[full_path] = last_modified

                else:
# unchanged → reuse
                    character = self._get_existing_character(full_path)

# fallback (safety)
                    if character is None:

                        logger.info(
                            f"Parsed character: "
                            f"{character.name}"
                        )

                        character = parse_txt(full_path)

                if character:
                    updated_characters.append(character)

            except Exception as e:
                print(f"[DataService] Error processing {file}: {e}")

            except Exception:

                logger.exception(
                    f"Error processing file: {file}"
                )

# Replace character list

        logger.info(
            f"Character scan complete: "
            f"{len(updated_characters)} "
            f"characters loaded"
        )

        self.characters = updated_characters

# --------------------------------------------------
# EXISTING CHARACTER LOOKUP
# --------------------------------------------------
    def _get_existing_character(self, file_path):

        for character in self.characters:
            if getattr(character, "source_file", None) == file_path:
                return character

        return None

# --------------------------------------------------
# DATA ACCESS
# --------------------------------------------------
    def get_characters(self):
        return self.characters

    def get_reputation(self):
        return self.reputation_data

# FILTERED REPUTATIONS FOR TOP PANEL
    def get_top_reputations(self):

        if not self.reputation_data:
            return []

        return [
            rep for rep in self.reputation_data
            if any(rep.name.startswith(prefix) for prefix in FEATURED_REPUTATIONS)
        ]

