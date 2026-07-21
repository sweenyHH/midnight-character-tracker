from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)

from app.ui.colors import CLASS_COLORS
from app.ui.character_table_helpers import (
    adjust_class_color,
)


class CharacterCard(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "overviewCard"
        )

        self.setFrameShape(
            QFrame.Box
        )

        layout = QVBoxLayout(self)

        self.name_label = QLabel()

        self.info_label = QLabel()

        self.ilvl_label = QLabel()

        layout.addWidget(
            self.name_label
        )

        layout.addWidget(
            self.info_label
        )

        layout.addWidget(
            self.ilvl_label
        )

    def set_character(
        self,
        character,
    ):

        class_name = getattr(
            character,
            "character_class",
            "-"
        )

        self.name_label.setText(
            f"<h2>{character.name}</h2>"
        )

        self.info_label.setText(
            f"<b>Level {getattr(character, 'level', '-')}</b> "
            f"<b>{getattr(character, 'race', '-')}</b> "
            f"<b>{class_name}</b> "
            f"<b>({getattr(character, 'specialization', '-')})</b>"
        )

        if class_name in CLASS_COLORS:

            adjusted = adjust_class_color(
                CLASS_COLORS[class_name]
            )

            self.info_label.setStyleSheet(
                f"color: {adjusted};"
            )

        else:

            self.info_label.setStyleSheet(
                ""
            )

        self.ilvl_label.setText(
            f"<b>Item Level:</b> "
            f"{getattr(character, 'avg_item_level', '-')}"
        )