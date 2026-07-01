from app.model.character import Character
from app.parser.currency_parser import parse_currency, parse_gold, parse_item, CURRENCY_GROUPS
from app.parser.reputation_parser import parse_reputation
from app.parser.section_parser import handle_section
from app.parser.equipment_parser import parse_equipment


FIELD_MAPPING = {
    "Character": "name",
    "Faction": "faction",
    "Race": "race",
    "Class": "character_class",
    "Specialization": "specialization",
    "Level": "level",

# ITEM LEVELS
    "Average Item Level": "avg_item_level",
    "Equipped Item Level": "equipped_item_level",
    "PvP Item Level": "pvp_item_level",

# Location
    "Zone": "zone",
    "Subzone": "subzone",
    "Coordinates": "coordinates",

# Stats
    "Primary Stat": "primary_stat",
    "Health": "health",
    "Armor": "armor",
}


def parse_txt(file_path):

    character_name = file_path.split("/")[-1].split(".")[0]
    character = Character(character_name)
    character.source_file = file_path

    current_section = None
    current_currency_group = None
    in_reputation_section = False
    in_equipment_section = False  

    reputations = []

# READ FILE ONCE
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

# PARSE EQUIPMENT (separate parser)
    character.equipment = parse_equipment(lines)


    print("DEBUG Equipment Count:", len(character.equipment))
    for e in character.equipment:
        print("  ", e.slot, "|", e.name)


# MAIN PARSING LOOP
    for line in lines:
        line = line.strip()

        if not line:
            continue

# -------------------------------
# EQUIPMENT SECTION (SKIP IN MAIN LOOP)
# -------------------------------
        if line == "Equipment:":
            in_equipment_section = True
            continue

        if in_equipment_section and (
            line.endswith(":") and line != "Equipment:"
        ):
            in_equipment_section = False

        if in_equipment_section:
            continue

# -------------------------------
# ENTER REPUTATION SECTION
# -------------------------------
        if line == "Reputations:":
            in_reputation_section = True
            continue

# -------------------------------
# EXIT REPUTATION SECTION
# -------------------------------

        if in_reputation_section and (
            line.endswith(":") and line != "Reputations:"
        or line.startswith("### USER_DATA")):
            in_reputation_section = False

# -------------------------------
# SECTION HEADERS
# -------------------------------
        if line == "== Primary Attributes ==":
            current_section = "attributes"
            continue

        if line == "== Combat Ratings ==":
            current_section = "combat_ratings"
            continue

# -------------------------------
# GROUP HEADERS (Currencies)
# -------------------------------
        if line.startswith("==") and line.endswith("=="):
            group_name = line.strip("=").strip()

            current_section = None

            if group_name in CURRENCY_GROUPS:
                current_currency_group = group_name
            else:
                current_currency_group = None

            continue

# -------------------------------
# VAULT PARSING 
# -------------------------------
        if line.startswith("Vault Row"):
            import re

            match = re.match(r"Vault Row (\d):\s*(.*)", line)

            if match:
                row_num = match.group(1)
                values_str = match.group(2)

                values = []

                if values_str:
                    for v in values_str.split(","):
                        v = v.strip()
                        if v.isdigit():
                            values.append(int(v))

                character.vault[f"row{row_num}"] = values

            continue

# -------------------------------
# GOLD
# -------------------------------
        if line.startswith("Gold:"):
            c = parse_gold(line)
            character.add_currency(c)
            continue

# -------------------------------
# CURRENCIES
# -------------------------------
        if "Quantity:" in line:
            c = parse_currency(line, current_currency_group)
            character.add_currency(c)
            continue

# -------------------------------
# ITEMS
# -------------------------------
        if line.startswith("["):
            c = parse_item(line, current_currency_group)
            if c:
                character.add_currency(c)
            continue

# -------------------------------
# REPUTATIONS
# -------------------------------
        if in_reputation_section:

    # protect against WeeklyDuties
            if "=" in line:
                continue

            try:
                rep = parse_reputation(line)

                if rep and rep.name:
                    reputations.append(rep)

            except:
                pass

            continue

# -------------------------------
# SECTION DATA
# -------------------------------
        if handle_section(line, current_section, character):
            continue

# -------------------------------
# GENERIC FIELDS
# -------------------------------
        if ":" in line:
            k, v = line.split(":", 1)

            if k.strip() in FIELD_MAPPING:
                value = v.strip()

                if value.replace(".", "", 1).isdigit():
                    value = float(value) if "." in value else int(value)

                setattr(character, FIELD_MAPPING[k.strip()], value)

    character.reputations = reputations
    return character
