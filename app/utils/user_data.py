# exxtracts data that has been entered by a user within the app and was not part of the pasted input from the character export addon

def extract_user_data(lines):

    start = None
    end = None

    for i, line in enumerate(lines):

        stripped = line.strip()

        if stripped == "### USER_DATA_START ###":
            start = i

        if stripped == "### USER_DATA_END ###":
            end = i
            break

    if start is not None and end is not None and end > start:
        return lines[start:end + 1]

    return []