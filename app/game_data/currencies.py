from app.game_data.currency_definition import (
    CurrencyDefinition,
)


GOLD = CurrencyDefinition(
    key="gold",
    currency_id=0,
    display_name="Gold",
)

BRIMMING_ARCANA = CurrencyDefinition(
    key="brimming_arcana",
    currency_id=3379,
    display_name="Brimming Arcana",
)

REMNANT_OF_ANGUISH = CurrencyDefinition(
    key="remnant_of_anguish",
    currency_id=3392,
    display_name="Remnant of Anguish",
)

VOIDLIGHT_MARL = CurrencyDefinition(
    key="voidlight_marl",
    currency_id=3316,
    display_name="Voidlight Marl",
)

ANGLER_PEARLS = CurrencyDefinition(
    key="angler_pearls",
    currency_id=3373,
    display_name="Angler Pearls",
)

UNDERCOIN = CurrencyDefinition(
    key="undercoin",
    currency_id=2803,
    display_name="Undercoin",
)

TIMEWARPED_BADGE = CurrencyDefinition(
    key="timewarped_badge",
    currency_id=1166,
    display_name="Timewarped Badge",
)

COMMUNITY_COUPONS = CurrencyDefinition(
    key="community_coupons",
    currency_id=3363,
    display_name="Community Coupons",
)

CONQUEST = CurrencyDefinition(
    key="conquest",
    currency_id=1602,
    display_name="Conquest",
)

HONOR = CurrencyDefinition(
    key="honor",
    currency_id=1792,
    display_name="Honor",
)

BLOODY_TOKEN = CurrencyDefinition(
    key="bloody_token",
    currency_id=2123,
    display_name="Bloody Token",
)


TRACKED_WARBAND_CURRENCIES = [
    GOLD,
    BRIMMING_ARCANA,
    REMNANT_OF_ANGUISH,
    VOIDLIGHT_MARL,

    ANGLER_PEARLS,
    UNDERCOIN,
    TIMEWARPED_BADGE,
    COMMUNITY_COUPONS,

    CONQUEST,
    HONOR,
    BLOODY_TOKEN,
]