"""
Parses the .txt character files into structured objects.
re module for regular expression (https://docs.python.org/3/library/re.html)
Character and Currency classes from app/model/character.py
"""

import re
from app.model.character import Character, Currency

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


def is_allowed_line(line: str) -> bool:
    """
    Checks whether a line should be parsed based on predefined prefixes.
    """
    return any(line.startswith(prefix) for prefix in ALLOWED_PREFIXES)


def parse_txt(file_path):
    """
    Parses a single TXT file and returns a Character object.
    Only selected lines are imported.
    """

# Extract character name from filename (fallback)

    character_name = file_path.split("/")[-1].split(".")[0]
    character = Character(character_name)
    character.source_file = file_path

    with open(file_path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

# Apply filter: skip everything not explicitly allowed
            if not is_allowed_line(line):
                continue
            
# Generic key-value parsing. Example: "Class: Paladin"
            
            if ":" in line and not "Quantity" in line:
                key, value = line.split(":", 1)

                key = key.strip()
                value = value.strip()

                # Store in character.location
                character.location[key] = value

                # Special case: overwrite character name
                if key == "Character":
                    character.name = value

                continue

# Currency parsing. Example:"Shard of Dundun (ID: 3376) - Quantity: 8/8"

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

    return character