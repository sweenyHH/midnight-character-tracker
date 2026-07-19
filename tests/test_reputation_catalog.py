from app.game_data.reputation_catalog import (
    get_reputation_by_id,
    get_reputation_by_key,
    get_reputation_by_name,
    is_featured_reputation,
)


# ==================================================
# ID LOOKUPS
# ==================================================

def test_lookup_by_id():

    rep = get_reputation_by_id(2704)

    assert rep is not None
    assert rep.key == "harati"


# ==================================================
# KEY LOOKUPS
# ==================================================

def test_lookup_by_key():

    rep = get_reputation_by_key(
        "harati"
    )

    assert rep is not None
    assert rep.key == "harati"


# ==================================================
# LOCALIZED NAME LOOKUPS
# ==================================================

def test_lookup_by_english_name():

    rep = get_reputation_by_name(
        "Hara'ti"
    )

    assert rep is not None
    assert rep.key == "harati"


def test_lookup_by_german_name():

    rep = get_reputation_by_name(
        "Die Singularität"
    )

    assert rep is not None
    assert rep.key == "the_singularity"


def test_lookup_by_french_name():

    rep = get_reputation_by_name(
        "Tribu des Amani"
    )

    assert rep is not None
    assert rep.key == "amani_tribe"


# ==================================================
# WARBAND-WIDE FLAG
# ==================================================

def test_warband_wide_reputation():

    rep = get_reputation_by_key(
        "council_of_dornogal"
    )

    assert rep is not None
    assert rep.warband_wide is True


def test_character_reputation():

    rep = get_reputation_by_key(
        "argent_crusade"
    )

    assert rep is not None
    assert rep.warband_wide is False


# ==================================================
# DEPRECATED FLAG
# ==================================================

def test_deprecated_reputation():

    rep = get_reputation_by_key(
        "arcane_thirst_silgryn_deprecated"
    )

    assert rep is not None
    assert rep.deprecated is True


def test_non_deprecated_reputation():

    rep = get_reputation_by_key(
        "argent_crusade"
    )

    assert rep is not None
    assert rep.deprecated is False


# ==================================================
# Featured FLAG
# ==================================================

def test_featured_reputation():

    rep = get_reputation_by_key(
        "ritual_sites"
    )

    assert rep is not None
    assert rep.featured is True

def test_non_featured_reputation():

    rep = get_reputation_by_key(
        "argent_crusade"
    )

    assert rep is not None
    assert rep.featured is False

def test_featured_lookup():

    assert is_featured_reputation(
        "ritual_sites"
    ) is True

    assert is_featured_reputation(
        "argent_crusade"
    ) is False