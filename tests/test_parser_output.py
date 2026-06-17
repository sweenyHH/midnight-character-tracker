
from app.parser.txt_parser import parse_txt


def test_parse_and_print_output():
    file_path = "import/test_character.txt"

    character = parse_txt(file_path)

    print("\n=== CHARACTER ===")
    print(f"Name: {character.name}")

    print("\n=== LOCATION / META ===")
    for key, value in character.location.items():
        print(f"{key}: {value}")

    print("\n=== CURRENCIES ===")
    for currency in character.currencies:
        print(
            f"{currency.name} -> {currency.quantity}"
            + (f"/{currency.max_value}" if currency.max_value else "")
        )

# Minimal assert for pytest to work
    assert character.name is not None
