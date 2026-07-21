from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)

from app.localization.ui_strings import (
    get_ui_string,
)


class PvpCard(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "overviewCard"
        )

        self.setFrameShape(
            QFrame.Box
        )

        layout = QVBoxLayout(self)

        self.pvp_title = QLabel()

        self.pvp_title.setObjectName(
            "overviewSectionTitle"
        )

        self.honor_level_label = QLabel()

        self.honor_progress_label = QLabel()

        layout.addWidget(
            self.pvp_title
        )

        layout.addWidget(
            self.honor_level_label
        )

        layout.addWidget(
            self.honor_progress_label
        )

    def set_character(
        self,
        character,
    ):

        self.pvp_title.setText(
            f"<h3>{get_ui_string('pvp')}</h3>"
        )

        self.honor_level_label.setText(
            f"{get_ui_string('honor_level')}: "
            f"{getattr(character, 'honor_level', '-')}"
        )

        if (
            character.honor_progress
            is not None
            and character.honor_progress_max
            is not None
        ):

            self.honor_progress_label.setText(
                f"{get_ui_string('honor_progress')}: "
                f"{character.honor_progress}"
                f"/"
                f"{character.honor_progress_max}"
            )

        else:

            self.honor_progress_label.setText(
                f"{get_ui_string('honor_progress')}: -"
            )

  