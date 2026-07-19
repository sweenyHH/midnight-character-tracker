from app.game_data.currency_catalog import (
    get_currency_by_id,
    get_currency_by_key,
    get_currency_by_name,
    is_featured_currency,
    get_featured_currencies,
    get_currency_display_name,
)


def test_lookup_by_id():

    currency = get_currency_by_id(
        3373
    )

    assert currency is not None
    assert (
        currency.key
        == "angler_pearls"
    )


def test_lookup_by_key():

    currency = get_currency_by_key(
        "angler_pearls"
    )

    assert currency is not None
    assert (
        currency.currency_id
        == 3373
    )


def test_lookup_by_english_name():

    currency = get_currency_by_name(
        "Angler Pearls"
    )

    assert currency is not None
    assert (
        currency.key
        == "angler_pearls"
    )


def test_lookup_by_german_name():

    currency = get_currency_by_name(
        "Anglerperlen"
    )

    assert currency is not None
    assert (
        currency.key
        == "angler_pearls"
    )


def test_lookup_by_french_name():

    currency = get_currency_by_name(
        "Perles de pêche"
    )

    assert currency is not None
    assert (
        currency.key
        == "angler_pearls"
    )


def test_featured_flag():

    currency = get_currency_by_key(
        "angler_pearls"
    )

    assert currency is not None
    assert currency.featured is True


def test_is_featured_currency():

    assert is_featured_currency(
        "angler_pearls"
    ) is True

def test_get_featured_currencies():

    currencies = (
        get_featured_currencies()
    )

    assert len(currencies) > 0

    assert any(
        currency.key == "angler_pearls"
        for currency in currencies
    )

def test_display_name_lookup():

    assert (
        get_currency_display_name(
            "angler_pearls"
        )
        == "Angler Pearls"
    )