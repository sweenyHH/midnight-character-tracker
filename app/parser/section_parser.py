# parses sections for attributes and combat rating

def _parse_combat_value(value_str):

# Parses values like: '918 rating / 24.96%'
# Returns: dict: { "rating": int | None, "percent": float | None }

    rating = None
    percent = None

    if "/" in value_str:
        parts = value_str.split("/")

# Left side: "918 rating"

        left = parts[0].strip().replace(" rating", "")
        if left.isdigit():
            rating = int(left)

# Right side: "24.96%"

        right = parts[1].strip().replace("%", "")
        try:
            percent = float(right)
        except ValueError:
            percent = None
    else:

# fallback if format is unexpected

        try:
            rating = int(value_str.strip())
        except ValueError:
            rating = None

    return {
        "rating": rating,
        "percent": percent
    }


def handle_section(line, current_section, character):

# -------------------------
# PRIMARY ATTRIBUTES
# -------------------------

    if current_section == "attributes" and ":" in line:
        k, v = line.split(":", 1)
        character.attributes[k.strip()] = v.strip()
        return True

# -------------------------
# COMBAT RATINGS
# -------------------------

    if current_section == "combat_ratings" and ":" in line:
        k, v = line.split(":", 1)

        key = k.strip()

# FILTER OUT WRONG ENTRIES
        if key in ["Currencies", "Currency Count"]:
            return True  # ignore silently

# STRUCTURED PARSING

        character.combat_ratings[key] = _parse_combat_value(v.strip())

        return True

# -------------------------
# MYTHIC+
# -------------------------

    if current_section == "mythic_plus":

        if line.startswith(
            "Overall Score:"
        ):

            try:
                character.mythic_score = int(
                    line.split(
                        ":",
                        1
                    )[1].strip()
                )

            except ValueError:
                pass

            return True

# -------------------------
# PVP
# -------------------------

    if current_section == "pvp":

        if line.startswith(
            "Honor Level:"
        ):

            try:

                character.honor_level = int(
                    line.split(
                        ":",
                        1
                    )[1].strip()
                )

            except ValueError:
                pass

            return True

        if line.startswith(
            "Honor Progress:"
        ):

            try:

                value = line.split(
                    ":",
                    1
                )[1].strip()

                current, maximum = value.split(
                    "/",
                    1
                )

                character.honor_progress = int(
                    current
                )

                character.honor_progress_max = int(
                    maximum
                )

            except ValueError:
                pass

            return True

    return False
