
import os
from app.parser.txt_parser import parse_txt


def create_test_file(tmp_path):
    content = """Character: Arthas
Class: Paladin
Level: 80

Gold: 500g 0s 0c

Shard of Dundun (ID: 3376) - Quantity: 4/8

[Amani Token] x3 (ID: 232875)
"""

    file_path = tmp_path / "arthas.txt"
    file_path.write_text(content, encoding="utf-8")
    return file_path


# -------------------------------
# Basic character parsing
# -------------------------------
def test_parse_basic_character(tmp_path):
    file_path = create_test_file(tmp_path)

    character, reputation = parse_txt(str(file_path))

    assert character.name == "Arthas"
    assert character.location["Class"] == "Paladin"
    assert character.location["Level"] == "80"


# -------------------------------
# Gold → converted to copper currency
# -------------------------------
def test_parse_gold_currency(tmp_path):
    file_path = create_test_file(tmp_path)

    character, _ = parse_txt(str(file_path))

    gold_currency = next(
        (c for c in character.currencies if c.name == "Gold"), None
    )

    assert gold_currency is not None
    assert gold_currency.quantity == 500 * 10000
    assert gold_currency.has_total_cap is False
    assert gold_currency.has_weekly_cap is False


# -------------------------------
# Only allowed items are parsed
# -------------------------------
def test_parse_allowed_item_only(tmp_path):
    content = """Character: Testy

[Good Item] x2 (ID: 232875)
[Bad Item] x5 (ID: 999999)
"""

    file_path = tmp_path / "items.txt"
    file_path.write_text(content, encoding="utf-8")

    character, _ = parse_txt(str(file_path))

    assert len(character.currencies) == 1

    item = character.currencies[0]
    assert item.name == "Spark of Radiance"
    assert item.quantity == 2


# -------------------------------
# Currency with total cap
# -------------------------------
def test_parse_currency_with_max(tmp_path):
    content = """Character: Arthas

Shard of Dundun (ID: 3376) - Quantity: 4/8
"""

    file_path = tmp_path / "currency.txt"
    file_path.write_text(content, encoding="utf-8")

    character, _ = parse_txt(str(file_path))

    currency = character.currencies[0]

    assert currency.name == "Shard of Dundun"
    assert currency.quantity == 4
    assert currency.max_total == 8
    assert currency.has_total_cap is True
    assert currency.has_weekly_cap is False


# -------------------------------
# Reputation (Renown)
# -------------------------------

def test_parse_reputation_renown(tmp_path):
    content = """Character: Testy

Amani Tribe Renown 12 300/2500
"""

    file_path = tmp_path / "rep.txt"
    file_path.write_text(content, encoding="utf-8")

    _, reputation = parse_txt(str(file_path))

    rep = reputation[0]

    assert rep.name == "Amani Tribe Renown 12 300/2500"
    assert rep.rep_type == "renown"
    assert rep.level == 12
    assert rep.current == 300
    assert rep.maximum == 2500



# -------------------------------
# Reputation (Standard)
# -------------------------------
def test_parse_reputation_standard(tmp_path):
    content = """Character: Testy

Blood Knights (Honored) 1200/6000
"""

    file_path = tmp_path / "rep_standard.txt"
    file_path.write_text(content, encoding="utf-8")

    _, reputation = parse_txt(str(file_path))

    rep = reputation[0]

    assert rep.name == "Blood Knights"
    assert rep.rep_type == "standard"
    assert rep.level == "Honored"
    assert rep.current == 1200
    assert rep.maximum == 6000


# -------------------------------
# All key-value lines are now kept
# -------------------------------
def test_keeps_all_key_value_lines(tmp_path):
    content = """Character: Testy
RandomStuff: ShouldBeKept
Unknown: 123
"""

    file_path = tmp_path / "no_filter.txt"
    file_path.write_text(content, encoding="utf-8")

    character, _ = parse_txt(str(file_path))

    assert character.name == "Testy"
    assert character.location["RandomStuff"] == "ShouldBeKept"
    assert character.location["Unknown"] == "123"


# -------------------------------
# Filename fallback
# -------------------------------
def test_filename_fallback(tmp_path):
    content = """Class: Mage"""

    file_path = tmp_path / "fallback_name.txt"
    file_path.write_text(content, encoding="utf-8")

    character, _ = parse_txt(str(file_path))

    assert character.name == "fallback_name"


# -------------------------------
# Robustness: ignore garbage safely
# -------------------------------
def test_handles_garbage_lines(tmp_path):
    content = """Character: Testy

This is random text
!!!$$$
"""

    file_path = tmp_path / "garbage.txt"
    file_path.write_text(content, encoding="utf-8")

    character, reputation = parse_txt(str(file_path))

    assert character.name == "Testy"
    assert len(character.currencies) == 0
    assert len(reputation) == 0

# -------------------------------
# Stress/fuzz test
# -------------------------------

def test_parser_does_not_crash_on_random_input(tmp_path):
    content = "\n".join(["random garbage line 123 !!!"] * 100)

    file_path = tmp_path / "stress.txt"
    file_path.write_text(content)

    character, reputation = parse_txt(str(file_path))

    assert character is not None


def test_reputation_filters_invalid_lines(tmp_path):
    content = """Character: Testy

The Singularity Champion (ID: 62265) - Points: 10
"""

    file_path = tmp_path / "rep_invalid.txt"
    file_path.write_text(content, encoding="utf-8")

    _, reputation = parse_txt(str(file_path))

    assert len(reputation) == 0

# Faction Test

def test_parse_faction(tmp_path):
    content = """Character: Testy
Faction: Alliance
"""

    file_path = tmp_path / "faction.txt"
    file_path.write_text(content, encoding="utf-8")

    character, _ = parse_txt(str(file_path))

    assert character.faction == "Alliance"



