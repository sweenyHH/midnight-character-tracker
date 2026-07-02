from app.model.character import (
    Character,
    Currency,
    Equipment,
)


# ==================================================
# Currency helper properties
# ==================================================

def test_currency_has_total_cap():

    currency = Currency(
        name="Test Currency",
        quantity=10,
        max_total=100,
    )

    assert currency.has_total_cap is True


def test_currency_no_total_cap():

    currency = Currency(
        name="Test Currency",
        quantity=10,
    )

    assert currency.has_total_cap is False


def test_currency_has_weekly_cap():

    currency = Currency(
        name="Test Currency",
        quantity=10,
        weekly_current=5,
        weekly_max=20,
    )

    assert currency.has_weekly_cap is True


def test_currency_no_weekly_cap():

    currency = Currency(
        name="Test Currency",
        quantity=10,
    )

    assert currency.has_weekly_cap is False


# ==================================================
# Character currency collection
# ==================================================

def test_add_currency():

    character = Character("Arthas")

    currency = Currency(
        name="Gold",
        quantity=5000000,
    )

    character.add_currency(currency)

    assert len(character.currencies) == 1
    assert character.currencies[0] is currency


# ==================================================
# Character equipment collection
# ==================================================

def test_add_equipment():

    character = Character("Arthas")

    item = Equipment(
        slot="Head",
        name="Helm of Testing",
        item_level=700,
    )

    character.add_equipment(item)

    assert len(character.equipment) == 1
    assert character.equipment[0] is item


# ==================================================
# Character defaults
# ==================================================

def test_character_defaults():

    character = Character("Arthas")

    assert character.name == "Arthas"

    assert character.faction is None
    assert character.character_class is None
    assert character.level is None

    assert character.currencies == []
    assert character.reputations == []
    assert character.equipment == []


# ==================================================
# Vault defaults
# ==================================================

def test_character_vault_defaults():

    character = Character("Arthas")

    assert character.vault == {
        "row1": [],
        "row2": [],
        "row3": [],
    }


# ==================================================
# Currency cap combinations
# ==================================================

def test_currency_can_have_both_caps():

    currency = Currency(
        name="Test Currency",
        quantity=50,
        max_total=100,
        weekly_current=10,
        weekly_max=20,
    )

    assert currency.has_total_cap is True
    assert currency.has_weekly_cap is True


# ==================================================
# Equipment fields
# ==================================================

def test_equipment_fields():

    item = Equipment(
        slot="Trinket",
        name="Orb of Testing",
        item_level=720,
        item_type="Epic",
        enchanted=True,
        quality="Epic",
    )

    assert item.slot == "Trinket"
    assert item.name == "Orb of Testing"
    assert item.item_level == 720
    assert item.item_type == "Epic"
    assert item.enchanted is True
    assert item.quality == "Epic"