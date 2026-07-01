import re
from app.model.character import Equipment


def parse_equipment(lines):

    equipment = []

    in_equipment_section = False
    current_slot = None
    current_item = None

    QUALITY_MAP = {
        "common": "common",
        "uncommon": "uncommon",
        "rare": "rare",
        "epic": "epic",
        "legendary": "legendary"
    }

    for i, raw_line in enumerate(lines):

        line = raw_line.strip()

        if not line:
            continue

# -------------------------------
# ENTER EQUIPMENT
# -------------------------------
        if line == "Equipment:":
            in_equipment_section = True
            continue

# -------------------------------
# EXIT EQUIPMENT
# -------------------------------
        if in_equipment_section:
            if (
                line.endswith(":")
                and not line.startswith("-")
                and not line.startswith("[")
                and not line.startswith("==")
                and line != "Equipment:"
            ):
                break

        if not in_equipment_section:
            continue

# -------------------------------
# SLOT HEADER
# -------------------------------
        if line.startswith("==") and line.endswith("=="):

            if current_item:
                equipment.append(current_item)
                current_item = None

            current_slot = line.strip("=").strip()
            continue

# -------------------------------
# ITEM LINE
# -------------------------------
        if current_slot and line.startswith("["):

            # Empty slot
            if line == "[Empty]":
                current_item = Equipment(
                    slot=current_slot,
                    name="Empty",
                    item_level=None,
                    item_type=None,
                    enchanted=False,
                    quality=None
                )
                continue

            name_match = re.match(r"\[(.*?)\]", line)
            ilvl_match = re.search(r"iLvl:\s*(\d+)", line)

            name = name_match.group(1) if name_match else "Unknown"
            item_level = int(ilvl_match.group(1)) if ilvl_match else None

            current_item = Equipment(
                slot=current_slot,
                name=name,
                item_level=item_level,
                item_type=None,
                enchanted=False,
                quality=None
            )

            continue

# -------------------------------
# ITEM DETAILS
# -------------------------------
        if current_item and line.startswith("-"):

            if line.startswith("- Type:"):
                current_item.item_type = line.split(":", 1)[1].strip()

            elif line.startswith("- Rarity:"):
                raw = line.split(":", 1)[1].strip().lower()
                current_item.quality = QUALITY_MAP.get(raw, None)

            elif line.startswith("- Enchant ID:"):
                current_item.enchanted = True

            continue

# -------------------------------
# SAVE LAST ITEM
# -------------------------------
    if current_item:
        equipment.append(current_item)

    return equipment

