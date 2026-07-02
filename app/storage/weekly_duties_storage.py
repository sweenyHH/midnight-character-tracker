from app.storage.user_data_storage import (
    load_section,
    save_section,
)

def load_state(file_path):

    result = {}

    lines = load_section(
        file_path,
        "WeeklyDuties"
    )

    for stripped in lines:

        if "=" not in stripped:
            continue

        k, v = stripped.split("=")
        result[k] = (v == "1")

    return result

def save_state(file_path, checkboxes):

    duty_lines = []

    for row_index, boxes in checkboxes:

        for i, cb in enumerate(boxes):

            if cb.isChecked():
                duty_lines.append(
                    f"{row_index}_{i}=1"
                )

    save_section(
        file_path,
        "WeeklyDuties",
        duty_lines
    )