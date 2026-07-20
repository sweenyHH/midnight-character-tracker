# --------------------------------------------------
# Blizzard Color Codes
# --------------------------------------------------
#
# Reusable Blizzard color definitions.
#
# Sources:
# - WoW item quality colors
# - Mythic+ rating colors
#
# Keep all Blizzard-related colors centralized here.
# --------------------------------------------------

# Item Quality / Mythic+ Threshold Colors

POOR = "#9D9D9D"
COMMON = "#FFFFFF"
UNCOMMON = "#1EFF00"
RARE = "#0070DD"
EPIC = "#A335EE"
LEGENDARY = "#FF8000"
ARTIFACT = "#E6CC80"


# --------------------------------------------------
# Mythic+
# --------------------------------------------------

MPLUS_THRESHOLDS = [
    (3000, ARTIFACT),
    (2500, LEGENDARY),
    (2000, EPIC),
    (1500, RARE),
    (1000, UNCOMMON),
]


def get_mplus_color(score):
    """
    Returns the Blizzard Mythic+ color
    matching the supplied score.

    Examples:

        3200 -> #E6CC80
        2700 -> #FF8000
        2100 -> #A335EE
        1600 -> #0070DD
        1200 -> #1EFF00
        500  -> #FFFFFF
    """

    if score is None:
        return COMMON

    for threshold, color in MPLUS_THRESHOLDS:

        if score >= threshold:
            return color

    return COMMON