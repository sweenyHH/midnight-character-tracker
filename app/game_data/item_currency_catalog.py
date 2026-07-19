import csv
from pathlib import Path

from app.game_data.item_currency_definition import (
    ItemCurrencyDefinition,
)


_ITEM_CURRENCIES_BY_ID = {}
_ITEM_CURRENCIES_BY_KEY = {}
_ITEM_CURRENCIES_BY_NAME = {}

def _to_bool(value):
    return str(value).strip().upper() == "TRUE"

_LOADED = False


def _load_catalog():

    global _LOADED

    if _LOADED:
        return

    csv_path = (
        Path(__file__).parent
        / "item_currencies.csv"
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

            definition = (
                ItemCurrencyDefinition(
                    item_id=int(
                        row["item_id"]
                    ),
                    key=row["key"],

                    english_name=row[
                        "english_name"
                    ],
                    german_name=row[
                        "german_name"
                    ],
                    french_name=row[
                        "french_name"
                    ],
                    featured=_to_bool(
                        row["featured"]
                        ),
                )
            )

            if (
                definition.item_id
                in _ITEM_CURRENCIES_BY_ID
            ):
                raise ValueError(
                    f"Duplicate item id: "
                    f"{definition.item_id}"
                )

            if (
                definition.key
                in _ITEM_CURRENCIES_BY_KEY
            ):
                raise ValueError(
                    f"Duplicate key: "
                    f"{definition.key}"
                )

            _ITEM_CURRENCIES_BY_ID[
                definition.item_id
            ] = definition

            _ITEM_CURRENCIES_BY_KEY[
                definition.key
            ] = definition

            for name in (
                definition.english_name,
                definition.german_name,
                definition.french_name,
            ):

                lookup_name = name.casefold()
                
                if lookup_name in _ITEM_CURRENCIES_BY_NAME:
                    raise ValueError(
                        f"Duplicate localized name: {name}"
                    )

                _ITEM_CURRENCIES_BY_NAME[
                    lookup_name
                ] = definition

    _LOADED = True


def get_item_currency_by_id(
    item_id,
):
    _load_catalog()

    return _ITEM_CURRENCIES_BY_ID.get(
        item_id
    )


def get_item_currency_by_key(
    key,
):
    _load_catalog()

    return _ITEM_CURRENCIES_BY_KEY.get(
        key
    )


def get_item_currency_by_name(
    name,
):
    _load_catalog()

    if not name:
        return None

    return _ITEM_CURRENCIES_BY_NAME.get(
        name.casefold()
    )

def is_featured_item_currency(
    key,
):
    _load_catalog()

    definition = (
        _ITEM_CURRENCIES_BY_KEY.get(
            key
        )
    )

    if definition is None:
        return False

    return definition.featured