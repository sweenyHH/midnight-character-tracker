from pathlib import Path

from app.parser.base_parser import parse_txt


DATA_DIR = Path(__file__).parent / "data"


def test_parse_full_character_identity():

    character = parse_txt(
        str(DATA_DIR / "full_character.txt")
    )

    assert character.name == "Testerella-The Tester Realm"
    assert character.faction == "Alliance"
    assert character.race == "Human"
    assert character.character_class == "Paladin"
    assert character.level == 90


def test_parse_full_character_item_levels():

    character = parse_txt(
        str(DATA_DIR / "full_character.txt")
    )

    assert character.avg_item_level == 278.94
    assert character.equipped_item_level == 278.94
    assert character.pvp_item_level == 278.94


def test_parse_gold_from_real_file():

    character = parse_txt(
        str(DATA_DIR / "full_character.txt")
    )

    gold = next(
        (c for c in character.currencies if c.name == "Gold"),
        None,
    )

    assert gold is not None
    assert gold.quantity == 10003882


def test_parse_currency_group_entry():

    character = parse_txt(
        str(DATA_DIR / "full_character.txt")
    )

    shard = next(
        (c for c in character.currencies if c.name == "Shard of Dundun"),
        None,
    )

    assert shard is not None
    assert shard.quantity == 8
    assert shard.max_total == 8
    assert shard.has_total_cap is True
    assert shard.has_weekly_cap is True


def test_parse_allowed_item_currencies_from_bags():

    character = parse_txt(
        str(DATA_DIR / "full_character.txt")
    )

    names = {c.name for c in character.currencies}

    assert "Spark of Radiance" in names
    assert "Ascendant Voidcore" in names
    assert "Ascendant Voidshard" in names


def test_parse_equipment():

    character = parse_txt(
        str(DATA_DIR / "full_character.txt")
    )

    assert len(character.equipment) > 0

    head = next(
        (
            item
            for item in character.equipment
            if item.slot == "Head"
        ),
        None,
    )

    assert head is not None
    assert head.name == "Luminant Verdict's Unwavering Gaze"


def test_parse_reputations():

    character = parse_txt(
        str(DATA_DIR / "full_character.txt")
    )

    assert len(character.reputations) > 20

    amani = next(
        (
            rep
            for rep in character.reputations
            if rep.name == "Amani Tribe"
        ),
        None,
    )

    assert amani is not None
    assert amani.rep_type == "renown"


def test_parser_ignores_user_data_sections():

    character = parse_txt(
        str(DATA_DIR / "character_with_userdata.txt")
    )

    currency_names = {
        c.name for c in character.currencies
    }

    reputation_names = {
        r.name for r in character.reputations
    }

    assert "Vault" not in currency_names
    assert "WeeklyDuties" not in currency_names
    assert "This is a testnote" not in reputation_names


def test_parser_handles_file_with_userdata():

    character = parse_txt(
        str(DATA_DIR / "character_with_userdata.txt")
    )

    assert character.name == "Testerus-The Testers Brotherhood"
    assert character.character_class == "Priest"
    assert character.faction == "Alliance"


def test_currency_groups_are_attached():

    character = parse_txt(
        str(DATA_DIR / "full_character.txt")
    )

    shard = next(
        (
            c
            for c in character.currencies
            if c.name == "Shard of Dundun"
        ),
        None,
    )

    assert shard is not None
    assert "Midnight" in shard.groups


def test_user_data_not_parsed_as_reputation():

    character = parse_txt(
        str(DATA_DIR / "character_with_userdata.txt")
    )

    names = [rep.name for rep in character.reputations]

    assert "Vault" not in names
    assert "WeeklyDuties" not in names


def test_debug_lines_not_imported_as_reputations():

    character = parse_txt(
        str(DATA_DIR / "character_with_userdata.txt")
    )

    names = [rep.name for rep in character.reputations]

    assert "[Debug] Retail reputation API entries: 168" not in names