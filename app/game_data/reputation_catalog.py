import csv
from pathlib import Path

from app.game_data.reputation_definition import (
    ReputationDefinition,
)


_REPUTATIONS_BY_ID = {}
_REPUTATIONS_BY_KEY = {}
_REPUTATIONS_BY_NAME = {}

_LOADED = False


def _to_bool(value):
    return str(value).strip().upper() == "TRUE"


def _load_catalog():

    global _LOADED

    if _LOADED:
        return

    csv_path = (
        Path(__file__).parent
        / "reputations.csv"
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

            definition = ReputationDefinition(
                faction_id=int(row["id"]),
                key=row["key"],

                english_name=row["english_name"],
                german_name=row["german_name"],
                french_name=row["french_name"],

                warband_wide=_to_bool(
                    row["warband_wide"]
                ),
                deprecated=_to_bool(
                    row["deprecated"]
                ),
                featured=_to_bool(
                    row["featured"]
                ),

            )


            # --------------------------------------------------
            # ID LOOKUP
            # --------------------------------------------------

            if (
                definition.faction_id
                in _REPUTATIONS_BY_ID
            ):
                raise ValueError(
                    f"Duplicate faction ID: "
                    f"{definition.faction_id}"
                )

            _REPUTATIONS_BY_ID[
                definition.faction_id
            ] = definition

            # --------------------------------------------------
            # KEY LOOKUP
            # --------------------------------------------------

            if (
                definition.key
                in _REPUTATIONS_BY_KEY
            ):
                raise ValueError(
                    f"Duplicate key: "
                    f"{definition.key}"
                )

            _REPUTATIONS_BY_KEY[
                definition.key
            ] = definition

            # --------------------------------------------------
            # NAME LOOKUPS
            # --------------------------------------------------

            for name in (
                definition.english_name,
                definition.german_name,
                definition.french_name,
            ):

                if not name:
                    continue

                _REPUTATIONS_BY_NAME[
                    name.casefold()
                ] = definition

    _LOADED = True


def get_reputation_by_id(faction_id):
    _load_catalog()
    return _REPUTATIONS_BY_ID.get(
        faction_id
    )


def get_reputation_by_key(key):
    _load_catalog()
    return _REPUTATIONS_BY_KEY.get(
        key
    )


def get_reputation_by_name(name):
    _load_catalog()

    if not name:
        return None

    return _REPUTATIONS_BY_NAME.get(
        name.casefold()
    )

def is_featured_reputation(key):
    _load_catalog()

    definition = _REPUTATIONS_BY_KEY.get(key)

    if definition is None:
        return False

    return definition.featured