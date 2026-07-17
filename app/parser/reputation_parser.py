import re
from app.model.reputation import Reputation


# Parsing of reputation lines and split depending on renown faction or other faction

def parse_reputation(line: str):
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

    return Reputation(name, typ, lvl, cur, maxv)