from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit
from .utils import get_layout
import json


class DebugTab(QWidget):

    def set_character(self, character):
        layout = get_layout(self)

# -------------------------
# BASIC INFO
# -------------------------

        layout.addWidget(QLabel("<b>Debug Information</b>"))
        layout.addWidget(QLabel(f"Name: {character.name}"))
        layout.addWidget(QLabel(f"Source file: {getattr(character, 'source_file', '-')}"))

        layout.addWidget(QLabel(f"Currencies: {len(character.currencies)}"))
        layout.addWidget(QLabel(f"Attributes: {len(getattr(character, 'attributes', {}))}"))
        layout.addWidget(QLabel(f"Combat stats: {len(getattr(character, 'combat_ratings', {}))}"))
        layout.addWidget(QLabel(f"Reputations: {len(getattr(character, 'reputations', []))}"))

# -------------------------
# STRUCTURED DATA VIEW
# -------------------------

        debug_output = QTextEdit()
        debug_output.setReadOnly(True)
        debug_output.setObjectName("debugOutput")

# Create structured dump
        data = {
            "name": character.name,
            "level": getattr(character, "level", None),
            "class": getattr(character, "character_class", None),
            "currencies_count": len(character.currencies),
            "attributes": character.attributes,
            "combat_ratings": character.combat_ratings,
        }

        try:
            formatted = json.dumps(data, indent=4)
        except Exception:
            formatted = str(data)

        debug_output.setText(formatted)

        layout.addWidget(QLabel("<b>Parsed Data (JSON)</b>"))
        layout.addWidget(debug_output)

        layout.addStretch()
