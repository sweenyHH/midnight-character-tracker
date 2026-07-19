from app.game_data.currency_catalog import get_featured_currencies

def get_warband_currency_totals(characters):

    featured_currencies = (get_featured_currencies())

    totals = {
        definition.key: 0
        for definition in featured_currencies
    }

    tracked_by_id = {
        definition.currency_id: definition
        for definition in featured_currencies
    }

    for character in characters:

        for currency in character.currencies:

            definition = tracked_by_id.get(
                currency.currency_id
            )

            if definition is None:
                continue

            totals[
                definition.key
            ] += (
                currency.quantity or 0
            )

    return totals