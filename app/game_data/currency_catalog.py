import csv
from pathlib import Path

from app.game_data.currency_catalog_definition import CurrencyCatalogDefinition



_CURRENCIES_BY_ID = {}
_CURRENCIES_BY_KEY = {}
_CURRENCIES_BY_NAME = {}

_LOADED = False


def _to_bool(value):
    return (
        str(value)
        .strip()
        .upper()
        == "TRUE"
    )


def _load_catalog():

    global _LOADED

    if _LOADED:
        return

    _CURRENCIES_BY_ID.clear()
    _CURRENCIES_BY_KEY.clear()
    _CURRENCIES_BY_NAME.clear()

    csv_path = (
        Path(__file__).parent
        / "currencies.csv"
    )

    with open(
        csv_path,
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(
            file,
            delimiter=";"
        )

        reader.fieldnames = [
            name.strip()
            for name in reader.fieldnames
        ]

        for row in reader:
            
            definition = CurrencyCatalogDefinition(
                currency_id=int(row["id"]),
                key=row["key"],

                english_name=row["english_name"],
                german_name=row["german_name"],
                french_name=row["french_name"],

                featured=_to_bool(row["featured"]),
            )

            if (
                definition.currency_id
                in _CURRENCIES_BY_ID
            ):
                raise ValueError(
                    f"Duplicate currency id: "
                    f"{definition.currency_id}"
                )

            if (
                definition.key
                in _CURRENCIES_BY_KEY
            ):
                raise ValueError(
                    f"Duplicate key: "
                    f"{definition.key}"
                )

            _CURRENCIES_BY_ID[
                definition.currency_id
            ] = definition

            _CURRENCIES_BY_KEY[
                definition.key
            ] = definition

            for name in (
                definition.english_name,
                definition.german_name,
                definition.french_name,
            ):

                lookup_name = (
                    name.casefold()
                )


                if (
                    lookup_name
                    not in _CURRENCIES_BY_NAME
                ):
                    _CURRENCIES_BY_NAME[
                        lookup_name
                    ] = definition

                _CURRENCIES_BY_NAME[
                    lookup_name
                ] = definition

    _LOADED = True


def get_currency_by_id(
    currency_id,
):
    _load_catalog()

    return _CURRENCIES_BY_ID.get(
        currency_id
    )


def get_currency_by_key(
    key,
):
    _load_catalog()

    return _CURRENCIES_BY_KEY.get(
        key
    )


def get_currency_by_name(
    name,
):
    _load_catalog()

    if not name:
        return None

    return _CURRENCIES_BY_NAME.get(
        name.casefold()
    )


def is_featured_currency(
    key,
):
    _load_catalog()

    definition = (
        _CURRENCIES_BY_KEY.get(key)
    )

    if definition is None:
        return False

    return definition.featured


def get_featured_currencies():

    _load_catalog()

    return [
        definition
        for definition
        in _CURRENCIES_BY_ID.values()
        if definition.featured
    ]

def get_currency_display_name(
    key,
):
    _load_catalog()

    definition = (
        _CURRENCIES_BY_KEY.get(key)
    )

    if definition is None:
        return key

    return definition.english_name