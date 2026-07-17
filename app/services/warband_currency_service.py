from app.game_data.currencies import (
    TRACKED_WARBAND_CURRENCIES,
)


def get_warband_currency_totals(characters):

    totals = {
        definition.display_name: 0
        for definition in TRACKED_WARBAND_CURRENCIES
    }

    tracked_by_id = {
        definition.currency_id: definition
        for definition in TRACKED_WARBAND_CURRENCIES
    }

    for character in characters:

        for currency in character.currencies:

            definition = tracked_by_id.get(
                currency.currency_id
            )

            if definition is None:
                continue

            totals[
                definition.display_name
            ] += (
                currency.quantity or 0
            )

    return totals