from app.model.character import Character
from app.parser.currency_parser import parse_currency, parse_gold, parse_item, CURRENCY_GROUPS
from app.parser.reputation_parser import is_reputation_line, parse_reputation
from app.parser.section_parser import handle_section


FIELD_MAPPING = {
    "Character": "name",
    "Class": "character_class",
    "Level": "level",
}


def parse_txt(file_path):

    character_name = file_path.split("/")[-1].split(".")[0]
    character = Character(character_name)
    character.source_file = file_path
    current_section = None
    current_currency_group = None


    reputations = []

    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

# SECTION HEADERS
            if line == "== Primary Attributes ==":
                current_section = "attributes"
                continue

            if line == "== Combat Ratings ==":
                current_section = "combat_ratings"
                continue

# GROUP HEADERS
            
            if line.startswith("==") and line.endswith("=="):
                group_name = line.strip("=").strip()


                current_section = None

                if group_name in CURRENCY_GROUPS:
                    current_currency_group = group_name
                else:
                    current_currency_group = None

                continue

# GOLD
            if line.startswith("Gold:"):
                c = parse_gold(line)
                character.add_currency(c)
                continue

# CURRENCIES
            if "Quantity:" in line:
                c = parse_currency(line, current_currency_group)
                character.add_currency(c)
                continue

# ITEMS
            if line.startswith("["):
                c = parse_item(line, current_currency_group)
                if c:
                    character.add_currency(c)
                continue

# REPUTATIONS
            if is_reputation_line(line):
                reputations.append(parse_reputation(line))
                continue

# SECTION DATA
            if handle_section(line, current_section, character):
                continue

# GENERIC FIELDS
            if ":" in line:
                k, v = line.split(":", 1)
                if k.strip() in FIELD_MAPPING:
                    setattr(character, FIELD_MAPPING[k.strip()], v.strip())

    character.reputations = reputations
    return character