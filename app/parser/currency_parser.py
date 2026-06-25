import re
from app.model.character import Currency
from app.parser.utils import extract_name, extract_quantity, extract_weekly, extract_gold


# Some currencies are items, stored in bags. (Blizz is annoying players with this since 2004...)

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


# Currency Groups for non physical currencies

CURRENCY_GROUPS = {
    "Midnight",
    "Season 1",
    "Miscellaneous",
    "Player vs. Player",
    "War Within",
    "Dragonflight",
    "Shadowlands",
    "Battle for Azeroth",
    "Legion",
    "Warlords of Draenor",
    "Burning Crusade",
}


# Special case gold, math for gold to copper

def parse_gold(line):
    value = line.split(":", 1)[1].strip()

    g = int(re.search(r"(\d+)g", value).group(1)) if re.search(r"(\d+)g", value) else 0
    s = int(re.search(r"(\d+)s", value).group(1)) if re.search(r"(\d+)s", value) else 0
    c = int(re.search(r"(\d+)c", value).group(1)) if re.search(r"(\d+)c", value) else 0

    total = g * 10000 + s * 100 + c

    return Currency(name="Gold", quantity=total)

# Currency parsing and treatment depending on normal currency or currency with total or weekly cap

def parse_currency(line, group):
    name_match = re.match(r"^(.+?) \(ID:", line)
    name = name_match.group(1).strip() if name_match else line

    quantity_match = re.search(r"Quantity:\s*(\d+)(?:/(\d+))?", line)

    quantity = int(quantity_match.group(1)) if quantity_match else 0
    max_total = int(quantity_match.group(2)) if quantity_match and quantity_match.group(2) else None

    weekly_match = re.search(r"Weekly:\s*(\d+)\s*/\s*(\d+)", line)
    weekly_current = int(weekly_match.group(1)) if weekly_match else None
    weekly_max = int(weekly_match.group(2)) if weekly_match else None

    c = Currency(
        name=name,
        quantity=quantity,
        max_total=max_total,
        weekly_current=weekly_current,
        weekly_max=weekly_max
    )

    c.groups = [group] if group else ["Other"]  

    return c

# Currency like item parsing

def parse_item(line, group):
    import re

    id_match = re.search(r"ID:\s*(\d+)", line)
    if not id_match:
        return None

    item_id = id_match.group(1)
    if item_id not in ALLOWED_ITEM_IDS:
        return None

    name_match = re.search(r"\[(.*?)\]", line)
    name = name_match.group(1) if name_match else "Unknown Item"
    name = SPECIAL_ITEM_NAMES.get(item_id, name)

    qty_match = re.search(r"x(\d+)", line)
    quantity = int(qty_match.group(1)) if qty_match else 0

    c = Currency(name=name, quantity=quantity)
    c.groups = [group or "Other"]
    return c