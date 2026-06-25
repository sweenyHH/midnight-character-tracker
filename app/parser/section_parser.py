
# parses sections for attributes and combat rating

def handle_section(line, current_section, character):
    if current_section == "attributes" and ":" in line:
        k, v = line.split(":", 1)
        character.attributes[k.strip()] = v.strip()
        return True

    if current_section == "combat_ratings" and ":" in line:
        k, v = line.split(":", 1)
        character.combat_ratings[k.strip()] = v.strip()
        return True

    return False
