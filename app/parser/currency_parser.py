import re

from app.model.currency import Currency
from app.game_data.currency_catalog import get_currency_by_id
from app.game_data.item_currency_catalog import get_item_currency_by_id



# Currency Groups for non physical currencies

CURRENCY_GROUPS = {
    "Midnight",
    "War Within",
    "Shadowlands",
    "Legion",
    "Mists of Pandaria",
    "Wrath of the Lich King",
    "Player vs. Player",

    "Season 1",
    "Dragonflight", 
    "Battle for Azeroth",
    "Warlords of Draenor",
    "Cataclysm",
    "Burning Crusade",
    "Miscellaneous",
}


# Special case gold, math for gold to copper

def parse_gold(line):
    value = line.split(":", 1)[1].strip()

    g = int(re.search(r"(\d+)g", value).group(1)) if re.search(r"(\d+)g", value) else 0
    s = int(re.search(r"(\d+)s", value).group(1)) if re.search(r"(\d+)s", value) else 0
    c = int(re.search(r"(\d+)c", value).group(1)) if re.search(r"(\d+)c", value) else 0

    total = g * 10000 + s * 100 + c

    definition = get_currency_by_id(0)

    return Currency(
        name="Gold",
        quantity=total,
        currency_id=0,
        currency_type="currency",
        currency_key=definition.key if definition else None,
    )

# Currency parsing and treatment depending on normal currency or currency with total or weekly cap

def parse_currency(line, group):
    name_match = re.match(r"^(.+?) \(ID:", line)
    id_match = re.search(r"ID:\s*(\d+)", line)
    currency_id = int(id_match.group(1)) if id_match else None
    name = name_match.group(1).strip() if name_match else line

    quantity_match = re.search(r"Quantity:\s*(\d+)(?:/(\d+))?", line)

    quantity = int(quantity_match.group(1)) if quantity_match else 0
    max_total = int(quantity_match.group(2)) if quantity_match and quantity_match.group(2) else None

    weekly_match = re.search(r"Weekly:\s*(\d+)\s*/\s*(\d+)", line)
    weekly_current = int(weekly_match.group(1)) if weekly_match else None
    weekly_max = int(weekly_match.group(2)) if weekly_match else None

    definition = get_currency_by_id(currency_id)

    c = Currency(
        name=name,
        quantity=quantity,
        max_total=max_total,
        weekly_current=weekly_current,
        weekly_max=weekly_max,
        currency_id=currency_id,
        currency_type="currency",
        currency_key=definition.key if definition else None,
    )

    c.groups = [group] if group else ["Other"]  

    return c

# Currency like item parsing

def parse_item(line, group):

    id_match = re.search(r"ID:\s*(\d+)", line,)

    if not id_match:
        return None

    item_id = int(id_match.group(1))

    definition = get_item_currency_by_id(item_id)

    if definition is None:
        return None

    qty_match = re.search(r"x(\d+)", line,)

    quantity = (
        int(qty_match.group(1))
        if qty_match
        else 0
    )

    c = Currency(
        name=definition.english_name,
        quantity=quantity,

        currency_id=item_id,
        currency_type="item",

        currency_key=definition.key,
    )

    c.groups = [group or "Other"]

    return c