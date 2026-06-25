
from app.parser.txt_parser import parse_txt


def test_parse_and_print_output():
    file_path = "import/test_character.txt"

    character, reputation = parse_txt(file_path)

    print("\n=== CHARACTER ===")
    print(f"Name: {character.name}")

    print("\n=== LOCATION / META ===")
    for key, value in character.location.items():
        print(f"{key}: {value}")

    print("\n=== CURRENCIES ===")
    for currency in character.currencies:
        output = f"{currency.name} -> {currency.quantity}"

        if currency.max_total:
            output += f"/{currency.max_total}"

        if currency.has_weekly_cap:
            output += f" (Weekly: {currency.weekly_current}/{currency.weekly_max})"

        print(output)

    print("\n=== REPUTATION ===")
    for rep in reputation:
        print(
            f"{rep.name} | Type: {rep.rep_type} | Level: {rep.level} "
            f"| Progress: {rep.current}/{rep.maximum}"
        )

    # Minimal assert for pytest to work
    assert character.name is not None

