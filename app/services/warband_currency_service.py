TRACKED_WARBAND_CURRENCIES = [
    "Gold",
    "Brimming Arcana",
    "Remnant of Anguish",
    "Void Marl",

    "Angler Pearls",
    "Undercoin",
    "Timewarped Badge",
    "Community Coupons",

    "Conquest",
    "Honor",
    "Bloody Token",
]


def get_warband_currency_totals(characters):

    totals = {
        name: 0
        for name in TRACKED_WARBAND_CURRENCIES
    }

    for character in characters:

        for currency in character.currencies:

            if currency.name not in totals:
                continue

            totals[currency.name] += (
                currency.quantity or 0
            )

    return totals