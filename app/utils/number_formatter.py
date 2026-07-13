from app.storage.settings_storage import load_setting


def format_number(value):

    number_format = load_setting(
        "number_format",
        "german"
    )

    if number_format == "english":
        return f"{value:,}"

    return f"{value:,}".replace(
        ",",
        "."
    )