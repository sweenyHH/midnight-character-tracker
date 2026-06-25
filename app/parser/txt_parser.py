"""
Parses the .txt character files into structured objects.
"""

import re
from app.model.character import Character, Currency, Reputation



# -------------------------------
# Reputation prefixes (filter)
# -------------------------------

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


# -------------------------------
# Allowed special item IDs
# -------------------------------

ALLOWED_ITEM_IDS = {
    "232875",
    "245345",
    "268650",
    "268552",
}

SPECIAL_ITEM_NAMES = {
    "232875": "Spark of Radiance",
    "268650": "Ascendant Voidshard",
    "268552": "Ascendant Voidcore",
    "245345": "Fused Vitality",
}


# -------------------------------
# Field mapping
# -------------------------------

FIELD_MAPPING = {
    "Character": "name",
    "Faction": "faction",
    "Race": "race",
    "Class": "character_class",
    "Specialization": "specialization",
    "Level": "level",

    "Zone": "zone",
    "Subzone": "subzone",
    "Map": "map",
    "Map ID": "map_id",
    "Parent Map": "parent_map",
    "Parent Map ID": "parent_map_id",
    "Coordinates": "coordinates",
    "Hearthstone Location": "hearthstone_location",

    "Primary Stat": "primary_stat",
    "Health": "health",
    "Armor": "armor",

    "Average Item Level": "avg_item_level",
    "Equipped Item Level": "equipped_item_level",
    "PvP Item Level": "pvp_item_level",

    "XP": "xp",
    "XP To Level": "xp_to_level",
    "XP Progress": "xp_progress",
}


# -------------------------------
# Reputation helper
# -------------------------------

def is_reputation_line(line: str) -> bool:
    if not any(line.startswith(prefix) for prefix in REPUTATION_PREFIXES):
        return False

    if "Renown" in line:
        return True

    level_match = re.search(r"\(([A-Za-z\s]+)\)", line)
    progress_match = re.search(r"\d+/\d+", line)

    if level_match and progress_match:
        level_text = level_match.group(1)
        if level_text.startswith("ID"):
            return False
        return True

    return False


# -------------------------------
# MAIN PARSER
# -------------------------------

def parse_txt(file_path):

    character_name = file_path.split("/")[-1].split(".")[0]
    character = Character(character_name)
    character.source_file = file_path

    reputation_data = []

    current_section = None
    current_currency_group = None

# State flag

    in_currencies_section = False


    with open(file_path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            print("[LINE READ]:", line)

            if not line:
                continue


# -------------------------------
# ENTER / EXIT CURRENCY SECTION ✅
# -------------------------------
            if line == "Currencies:":
                in_currencies_section = True
                current_currency_group = None
                continue

            if line in ["Bags:", "Bank:", "Reputations:"]:
                in_currencies_section = False
                current_currency_group = None
                continue


            # -------------------------------
            # SECTION DETECTION (ATTRIBUTES)
            # -------------------------------
            if "== Primary Attributes ==" in line:
                current_section = "attributes"
                current_currency_group = None
                continue

            if "== Combat Ratings ==" in line:
                current_section = "combat_ratings"
                current_currency_group = None
                continue


            # -------------------------------
            # CURRENCY GROUP HEADERS ✅
            # -------------------------------
            if line.startswith("==") and line.endswith("=="):
                group_name = line.strip("=").strip()

                if in_currencies_section:
                    current_currency_group = group_name
                else:
                    current_currency_group = None

                current_section = None
                continue


            if line.startswith("==") and line.endswith("=="):
                group_name = line.strip("=").strip()

                if in_currencies_section:
                    current_currency_group = group_name
                else:
                    current_currency_group = None

                current_section = None
                continue

            # -------------------------------
            # IGNORE HEADERS
            # -------------------------------

            if line == "Currencies:":
                in_currencies_section = True
                current_currency_group = None
                continue

            if line in ["Bags:", "Bank:", "Reputations:"]:
                in_currencies_section = False
                current_currency_group = None
                continue


            # -------------------------------
            # GOLD
            # -------------------------------
            if line.startswith("Gold:"):
                value = line.split(":", 1)[1].strip()

                g = int(re.search(r"(\d+)g", value).group(1)) if re.search(r"(\d+)g", value) else 0
                s = int(re.search(r"(\d+)s", value).group(1)) if re.search(r"(\d+)s", value) else 0
                c = int(re.search(r"(\d+)c", value).group(1)) if re.search(r"(\d+)c", value) else 0

                total = g * 10000 + s * 100 + c

                currency = Currency(name="Gold", quantity=total)

                if current_currency_group:
                    currency.groups.append(current_currency_group)

                character.add_currency(currency)
                continue

            # -------------------------------
            # VAULT
            # -------------------------------
            if line.startswith("Vault Row"):
                match = re.match(r"Vault Row (\d):\s*(.*)", line)

                if match:
                    row = match.group(1)
                    values = [int(v.strip()) for v in match.group(2).split(",") if v.strip().isdigit()]
                    character.vault[f"row{row}"] = values

                continue

            # -------------------------------
            # ✅ MAIN CURRENCY PARSER (FIXED)
            # -------------------------------
            if "Quantity:" in line:
                print("✅ CURRENCY HIT:", line)

                name_match = re.match(r"^(.+?) \(ID:", line)
                name = name_match.group(1).strip() if name_match else line

                quantity_match = re.search(r"Quantity:\s*(\d+)(?:/(\d+))?", line)

                quantity = int(quantity_match.group(1)) if quantity_match else 0
                max_total = int(quantity_match.group(2)) if quantity_match and quantity_match.group(2) else None

                weekly_match = re.search(r"Weekly:\s*(\d+)\s*/\s*(\d+)", line)
                weekly_current = int(weekly_match.group(1)) if weekly_match else None
                weekly_max = int(weekly_match.group(2)) if weekly_match else None

                currency = Currency(
                    name=name,
                    quantity=quantity,
                    max_total=max_total,
                    weekly_current=weekly_current,
                    weekly_max=weekly_max
                )

                currency.groups.append(current_currency_group or "Other")

                character.add_currency(currency)
                continue

            # -------------------------------
            # ITEM PARSING
            # -------------------------------
            if line.startswith("[") and " x" in line:

                id_match = re.search(r"ID:\s*(\d+)", line)
                if not id_match:
                    continue

                item_id = id_match.group(1)

                if item_id not in ALLOWED_ITEM_IDS:
                    continue

                name_match = re.search(r"\[(.*?)\]", line)
                name = name_match.group(1) if name_match else "Unknown Item"

                name = SPECIAL_ITEM_NAMES.get(item_id, name)

                qty_match = re.search(r"x(\d+)", line)
                quantity = int(qty_match.group(1)) if qty_match else 0

                currency = Currency(name=name, quantity=quantity)

                if current_currency_group:
                    currency.groups.append(current_currency_group)

                character.add_currency(currency)
                continue

            # -------------------------------
            # REPUTATIONS (AFTER!)
            # -------------------------------
            if is_reputation_line(line):
                print("⚠️ REPUTATION MATCH:", line)

                name = line.split("(")[0].strip()

                renown = re.search(r"Renown\s+(\d+)", line)
                progress = re.search(r"(\d+)/(\d+)", line)

                lvl = int(renown.group(1)) if renown else None
                typ = "renown" if renown else "standard"

                if not renown:
                    lvl_match = re.search(r"\(([^)]+)\)", line)
                    lvl = lvl_match.group(1) if lvl_match else None

                cur = int(progress.group(1)) if progress else None
                maxv = int(progress.group(2)) if progress else None

                reputation_data.append(
                    Reputation(name, typ, lvl, cur, maxv)
                )
                continue

            # -------------------------------
            # SECTION CONTENT
            # -------------------------------
            if current_section == "attributes" and ":" in line:
                k, v = line.split(":", 1)
                character.attributes[k.strip()] = v.strip()
                continue

            if current_section == "combat_ratings" and ":" in line:
                k, v = line.split(":", 1)
                character.combat_ratings[k.strip()] = v.strip()
                continue

            # -------------------------------
            # GENERIC FIELDS
            # -------------------------------
            if ":" in line:
                k, v = line.split(":", 1)
                k, v = k.strip(), v.strip()

                if k in FIELD_MAPPING:
                    attr = FIELD_MAPPING[k]
                    if v.replace(".", "", 1).isdigit():
                        v = float(v) if "." in v else int(v)
                    setattr(character, attr, v)

    character.reputations = reputation_data

    return character