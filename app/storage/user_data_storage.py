import os

from app.services.internal_write_guard import write_guard


USER_START = "### USER_DATA_START ###"
USER_END = "### USER_DATA_END ###"


# ==================================================
# LOAD ALL SECTIONS
# ==================================================

def load_all_sections(file_path):

    sections = {}

    if not file_path or not os.path.exists(file_path):
        return sections

    current_section = None
    in_user_block = False

    with open(file_path, encoding="utf-8") as f:

        for line in f:

            stripped = line.strip()

            if stripped == USER_START:
                in_user_block = True
                continue

            if stripped == USER_END:
                break

            if not in_user_block:
                continue

            # section header
            if stripped.endswith(":") and "=" not in stripped:

                section_name = stripped[:-1]

                sections[section_name] = []
                current_section = section_name

                continue

            if current_section:
                sections[current_section].append(
                    stripped
                )

    return sections


# ==================================================
# LOAD SINGLE SECTION
# ==================================================

def load_section(file_path, section_name):

    sections = load_all_sections(file_path)

    return sections.get(section_name, [])


# ==================================================
# SAVE SINGLE SECTION
# ==================================================

def save_section(file_path, section_name, section_lines):

    if not file_path or not os.path.exists(file_path):
        return

    # -------------------------------
    # Read file
    # -------------------------------
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

    # -------------------------------
    # Preserve import data
    # -------------------------------
    import_lines = []

    in_user_block = False

    for line in lines:

        stripped = line.strip()

        if stripped == USER_START:
            in_user_block = True
            continue

        if stripped == USER_END:
            in_user_block = False
            continue

        if not in_user_block:
            import_lines.append(line)

    # -------------------------------
    # Load existing sections
    # -------------------------------
    sections = load_all_sections(file_path)

    # update section
    if section_lines:
        sections[section_name] = section_lines

    elif section_name in sections:
        del sections[section_name]

    # -------------------------------
    # Write file
    # -------------------------------
    with open(file_path, "w", encoding="utf-8") as f:

# Remove trailing empty lines before USER_DATA block
        while import_lines and not import_lines[-1].strip():
            import_lines.pop()

        f.writelines(import_lines)

        if sections:

            f.write("\n")
            f.write(USER_START + "\n")

            for name, lines in sections.items():

                f.write(f"{name}:\n")

                for line in lines:
                    f.write(line.rstrip("\n") + "\n")

            f.write(USER_END + "\n")

    write_guard.register_write(file_path)


# ==================================================
# USER BLOCK EXTRACTION
# ==================================================

def load_user_section(file_path):

    if not file_path or not os.path.exists(file_path):
        return []

    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

    start = None
    end = None

    for i, line in enumerate(lines):

        stripped = line.strip()

        if stripped == USER_START:
            start = i

        if stripped == USER_END:
            end = i
            break

    if start is not None and end is not None and end > start:
        return lines[start:end + 1]

    return []


def has_user_data(file_path):
    return bool(load_user_section(file_path))


def extract_user_data(lines):

    start = None
    end = None

    for i, line in enumerate(lines):

        stripped = line.strip()

        if stripped == USER_START:
            start = i

        if stripped == USER_END:
            end = i
            break

    if start is not None and end is not None and end > start:
        return lines[start:end + 1]

    return []