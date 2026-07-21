from app.localization.ui_strings import (
    get_ui_string,
)

GROUP_ORDER = [
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
    "Other",
]


def get_group_display_name(group_name):

    mapping = {
        "Player vs. Player":
            get_ui_string(
                "player_vs_player"
            ),

        "Miscellaneous":
            get_ui_string(
                "miscellaneous"
            ),

        "Other":
            get_ui_string(
                "other"
            ),

        "Season 1":
            get_ui_string(
                "season_1"
            ),
    }

    return mapping.get(group_name, group_name)