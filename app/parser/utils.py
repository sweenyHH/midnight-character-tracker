import re


# Extracts the name before (ID: ...)

def extract_name(line: str):

    match = re.match(r"^(.+?) \(ID:", line)
    return match.group(1).strip() if match else line


# Extracts quantity and optional max_total
# Example: Quantity: 10/100

def extract_quantity(line: str):

    match = re.search(r"Quantity:\s*(\d+)(?:/(\d+))?", line)

    if not match:
        return 0, None

    quantity = int(match.group(1))
    max_total = int(match.group(2)) if match.group(2) else None

    return quantity, max_total


# Extracts weekly values if present
# Example: Weekly: 0/600

def extract_weekly(line: str):

    match = re.search(r"Weekly:\s*(\d+)\s*/\s*(\d+)", line)

    if not match:
        return None, None

    return int(match.group(1)), int(match.group(2))

# Extracts gold/silver/copper and returns total copper

def extract_gold(value: str):

    g_match = re.search(r"(\d+)g", value)
    s_match = re.search(r"(\d+)s", value)
    c_match = re.search(r"(\d+)c", value)

    g = int(g_match.group(1)) if g_match else 0
    s = int(s_match.group(1)) if s_match else 0
    c = int(c_match.group(1)) if c_match else 0

    return g * 10000 + s * 100 + c