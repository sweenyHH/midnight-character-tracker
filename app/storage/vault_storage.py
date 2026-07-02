import os

from app.storage.user_data_storage import load_section


def load_user_vault(character):

    vault = getattr(
        character,
        "vault",
        {"row1": [], "row2": [], "row3": []}
    )

    lines = load_section(
        getattr(character, "source_file", None),
        "Vault"
    )

    if not lines:
        return vault

    user_vault = {
        "row1": [],
        "row2": [],
        "row3": []
    }

    for stripped in lines:

        if "=" not in stripped:
            continue

        key, value = stripped.split("=")

        row_idx, col_idx = key.split("_")
        row_name = f"row{int(row_idx) + 1}"

        while len(user_vault[row_name]) <= int(col_idx):
            user_vault[row_name].append(None)

        user_vault[row_name][int(col_idx)] = value

    if any(user_vault[r] for r in user_vault):
        return user_vault

    return vault