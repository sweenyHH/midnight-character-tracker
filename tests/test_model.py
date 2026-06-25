
import pytest
from app.model.character import Character, Currency


# -------------------------------
# Currency initialization
# -------------------------------
def test_currency_initialization():
    currency = Currency(
        "Gold",
        100,
        max_total=1000,
        weekly_current=50,
        weekly_max=500
    )

    assert currency.name == "Gold"
    assert currency.quantity == 100
    assert currency.max_total == 1000
    assert currency.weekly_current == 50
    assert currency.weekly_max == 500


# -------------------------------
# Currency without caps
# -------------------------------
def test_currency_without_caps():
    currency = Currency("Shard", 5)

    assert currency.name == "Shard"
    assert currency.quantity == 5
    assert currency.max_total is None
    assert currency.weekly_current is None
    assert currency.weekly_max is None


# -------------------------------
# Helper properties
# -------------------------------
def test_currency_helper_properties():
    currency = Currency(
        "Valor",
        10,
        max_total=100,
        weekly_current=5,
        weekly_max=20
    )

    assert currency.has_total_cap is True
    assert currency.has_weekly_cap is True


def test_currency_helper_properties_no_caps():
    currency = Currency("Simple", 1)

    assert currency.has_total_cap is False
    assert currency.has_weekly_cap is False


# -------------------------------
# Character initialization
# -------------------------------
def test_character_initialization():
    character = Character("TestChar")

    assert character.name == "TestChar"
    assert character.location == {}
    assert character.currencies == []


# -------------------------------
# Adding currency
# -------------------------------
def test_add_currency():
    character = Character("TestChar")
    currency = Currency("Gold", 200)

    character.add_currency(currency)

    assert len(character.currencies) == 1
    assert character.currencies[0].name == "Gold"
    assert character.currencies[0].quantity == 200
