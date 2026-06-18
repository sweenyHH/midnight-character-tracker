"""
Parses the .txt character files into structured objects.
re module for regular expression (https://docs.python.org/3/library/re.html)
Character and Currency classes from app/model/character.py
"""

import re
from app.model.character import Character, Currency, Reputation

"""
-------------------------------
FILTER CONFIGURATION
-------------------------------
Defines which lines should be parsed. Started with few lines, will be extended later.
"""

ALLOWED_PREFIXES = [

# Character Details

    "Character:",
    "Faction:",
    "Class:",
    "Average Item Level:",
    "Level:",
    "Specialization:",

# Currencies

    "Shard of Dundun (ID: 3376)",
    "Gold:",
    "Voidlight Marl",
    "Coffer Key Shards",
    "Restored Coffer Key",
    "Myth Dawncrest (ID: 3347)",
    "Brimming Arcana", 
    "Field Accolade", 
    "Luminous Dust", 
    "Remnant of Anguish", 
    "Shard of Dundun", 
    "Unalloyed Abundance", 
    "Uncontaminated Void Sample", 
    "Dawnlight Manaflux", 
    "Nebulous Voidcore", 
    "Undercoin",
    "Untainted Mana-Crystals", 
    "Adventurer Dawncrest", 
    "Veteran Dawncrest", 
    "Champion Dawncrest",
    "Hero Dawncrest", 
    "Myth Dawncrest", 
    "Radiant Spark Dust",    

# Reputations

    "Amani Tribe", 
    "Hara'ti",
    "Prey: Season 1",
    "Ritual Sites",
    "Silvermoon Court",
    "The Singularity",
    "Blood Knights",
    "Farstriders",
    "Magisters",
    "Shades of the Row",
    "Slayer's Duellum",
    "Valeera Sanguinar", 
]

# Dedicated list for reputation prefixes

REPUTATION_PREFIXES = [
    "Amani Tribe", 
    "Hara'ti",
    "Prey: Season 1",
    "Ritual Sites",
    "Silvermoon Court",
    "The Singularity",
    "Blood Knights",
    "Farstriders",
    "Magisters",
    "Shades of the Row",
    "Slayer's Duellum",
    "Valeera Sanguinar",
]


def is_allowed_line(line: str) -> bool:
    return any(line.startswith(prefix) for prefix in ALLOWED_PREFIXES)


def parse_txt(file_path):

# Extract character name from filename (fallback)

    character_name = file_path.split("/")[-1].split(".")[0]
    character = Character(character_name)
    character.source_file = file_path

# Store reputation globally

    reputation_data = []

    with open(file_path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

# Apply filter

            if not is_allowed_line(line):
                continue

# -------------------------------
# Reputation parsing
# -------------------------------

            if any(line.startswith(prefix) for prefix in REPUTATION_PREFIXES):

# Extract name

                name_match = re.match(r"^([^(]+)", line)
                name = name_match.group(1).strip() if name_match else line

# Case 1: Renown

                renown_match = re.search(r"Renown\s+(\d+)", line)

                if renown_match:
                    renown_level = int(renown_match.group(1))

                    progress_match = re.search(r"(\d+)/(\d+)", line)
                    current = maximum = None

                    if progress_match:
                        current = int(progress_match.group(1))
                        maximum = int(progress_match.group(2))

                    reputation_data.append(Reputation(
                        name=name,
                        rep_type="renown",
                        level=renown_level,
                        current=current,
                        maximum=maximum
                    ))

                    continue

# Case 2: Standard reputation

                level_match = re.search(r"\(([^)]+)\)", line)
                progress_match = re.search(r"(\d+)/(\d+)", line)

                level = level_match.group(1) if level_match else None

                current = maximum = None
                if progress_match:
                    current = int(progress_match.group(1))
                    maximum = int(progress_match.group(2))

                reputation_data.append(Reputation(
                    name=name,
                    rep_type="standard",
                    level=level,
                    current=current,
                    maximum=maximum
                ))

                continue

# -------------------------------
# Generic key-value parsing
# -------------------------------

            if ":" in line and "Quantity" not in line:
                key, value = line.split(":", 1)

                character.location[key.strip()] = value.strip()

                if key.strip() == "Character":
                    character.name = value.strip()

                continue

# -------------------------------
# Currency parsing
# -------------------------------

            match = re.match(r"(.+?) \(ID: \d+\) - Quantity: ([0-9/]+)", line)

            if match:
                name = match.group(1)
                quantity_text = match.group(2)

                if "/" in quantity_text:
                    current, max_value = quantity_text.split("/")
                    currency = Currency(
                        name=name,
                        quantity=int(current),
                        max_value=int(max_value),
                        category="Filtered"
                    )
                else:
                    currency = Currency(
                        name=name,
                        quantity=int(quantity_text),
                        category="Filtered"
                    )

                character.add_currency(currency)

    return character, reputation_data