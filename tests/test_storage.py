from app.storage.user_data_storage import (
    load_all_sections,
    load_section,
    save_section,
)


def create_test_file(tmp_path):
    content = """Character: Arthas
Class: Paladin
Level: 80
"""

    file_path = tmp_path / "arthas.txt"
    file_path.write_text(content, encoding="utf-8")

    return str(file_path)


# ==================================================
# SAVE + LOAD NOTES
# ==================================================

def test_save_and_load_notes(tmp_path):

    file_path = create_test_file(tmp_path)

    save_section(
        file_path,
        "Notes",
        ["Test note"]
    )

    notes = load_section(
        file_path,
        "Notes"
    )

    assert notes == ["Test note"]


# ==================================================
# NOTES PRESERVE VAULT
# ==================================================

def test_save_notes_preserves_vault(tmp_path):

    file_path = create_test_file(tmp_path)

    save_section(
        file_path,
        "Vault",
        [
            "0_0=272",
            "1_0=278",
        ]
    )

    save_section(
        file_path,
        "Notes",
        [
            "Important note"
        ]
    )

    vault = load_section(
        file_path,
        "Vault"
    )

    notes = load_section(
        file_path,
        "Notes"
    )

    assert vault == [
        "0_0=272",
        "1_0=278",
    ]

    assert notes == [
        "Important note"
    ]


# ==================================================
# VAULT PRESERVES NOTES
# ==================================================

def test_save_vault_preserves_notes(tmp_path):

    file_path = create_test_file(tmp_path)

    save_section(
        file_path,
        "Notes",
        [
            "Test note"
        ]
    )

    save_section(
        file_path,
        "Vault",
        [
            "0_0=265",
            "0_1=268",
        ]
    )

    notes = load_section(
        file_path,
        "Notes"
    )

    vault = load_section(
        file_path,
        "Vault"
    )

    assert notes == [
        "Test note"
    ]

    assert vault == [
        "0_0=265",
        "0_1=268",
    ]


# ==================================================
# WEEKLY DUTIES PRESERVE BOTH
# ==================================================

def test_weekly_duties_preserve_other_sections(tmp_path):

    file_path = create_test_file(tmp_path)

    save_section(
        file_path,
        "Notes",
        [
            "Weekly reset reminder"
        ]
    )

    save_section(
        file_path,
        "Vault",
        [
            "0_0=272"
        ]
    )

    save_section(
        file_path,
        "WeeklyDuties",
        [
            "0_0=1",
            "0_1=1",
        ]
    )

    sections = load_all_sections(
        file_path
    )

    assert sections["Notes"] == [
        "Weekly reset reminder"
    ]

    assert sections["Vault"] == [
        "0_0=272"
    ]

    assert sections["WeeklyDuties"] == [
        "0_0=1",
        "0_1=1",
    ]


# ==================================================
# REMOVE NOTES ONLY
# ==================================================

def test_remove_notes_preserves_other_sections(tmp_path):

    file_path = create_test_file(tmp_path)

    save_section(
        file_path,
        "Notes",
        [
            "Temporary note"
        ]
    )

    save_section(
        file_path,
        "Vault",
        [
            "0_0=272"
        ]
    )

    save_section(
        file_path,
        "Notes",
        []
    )

    notes = load_section(
        file_path,
        "Notes"
    )

    vault = load_section(
        file_path,
        "Vault"
    )

    assert notes == []

    assert vault == [
        "0_0=272"
    ]


# ==================================================
# LOAD ALL SECTIONS
# ==================================================

def test_load_all_sections(tmp_path):

    file_path = create_test_file(tmp_path)

    save_section(
        file_path,
        "Notes",
        [
            "Test note"
        ]
    )

    save_section(
        file_path,
        "WeeklyDuties",
        [
            "0_0=1"
        ]
    )

    save_section(
        file_path,
        "Vault",
        [
            "0_0=272"
        ]
    )

    sections = load_all_sections(
        file_path
    )

    assert set(sections.keys()) == {
        "Notes",
        "WeeklyDuties",
        "Vault",
    }


# ==================================================
# IMPORT DATA SURVIVES
# ==================================================

def test_import_section_is_preserved(tmp_path):

    file_path = create_test_file(tmp_path)

    save_section(
        file_path,
        "Notes",
        [
            "Test note"
        ]
    )

    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    assert "Character: Arthas" in content
    assert "Class: Paladin" in content
    assert "Level: 80" in content

    assert "Notes:" in content


# ==================================================
# EMPTY FILE DOES NOT CRASH
# ==================================================

def test_loading_missing_section_returns_empty(tmp_path):

    file_path = create_test_file(tmp_path)

    result = load_section(
        file_path,
        "Vault"
    )

    assert result == []