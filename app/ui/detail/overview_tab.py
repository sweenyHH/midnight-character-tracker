from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

from app.ui.colors import CLASS_COLORS
from app.ui.character_table_helpers import (
    adjust_class_color,
)
from app.ui.blizzard_color_codes import get_mplus_color
from app.game_data.currency_catalog import get_currency_display_name

from app.services.display_language import get_display_language


class OverviewTab(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.name_label = QLabel()
        self.info_label = QLabel()
        self.ilvl_label = QLabel()

        self.mythic_title = QLabel("<h3>Mythic+</h3>")
        self.mythic_score_label = QLabel()

        self.pvp_title = QLabel("<h3>PvP</h3>")
        self.honor_level_label = QLabel()
        self.honor_progress_label = QLabel()

        self.resources_title = QLabel(
            "<h3>Character Resources</h3>"
        )

        self.coffer_keys_label = QLabel()
        self.undercoin_label = QLabel()
        self.spark_label = QLabel()

        layout.addWidget(self.name_label)
        layout.addWidget(self.info_label)
        layout.addWidget(self.ilvl_label)

        layout.addWidget(self.mythic_title)
        layout.addWidget(self.mythic_score_label)

        layout.addWidget(self.pvp_title)
        layout.addWidget(self.honor_level_label)
        layout.addWidget(self.honor_progress_label)

        layout.addWidget(self.resources_title)

        layout.addWidget(self.coffer_keys_label)
        layout.addWidget(self.undercoin_label)
        layout.addWidget(self.spark_label)

        layout.addStretch()

    def set_character(self, character):

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

            self.info_label.setStyleSheet("")

        self.ilvl_label.setText(
            f"<b>Item Level:</b> "
            f"{getattr(character, 'avg_item_level', '-')}"
        )

        score = getattr(
            character,
            "mythic_score",
            None,
        )

        self.mythic_score_label.setText(
            f"Score: {score}"
        )

        self.mythic_score_label.setStyleSheet(
            f"color: {get_mplus_color(score)};"
        )

        self.honor_level_label.setText(
            f"Honor Level: "
            f"{getattr(character, 'honor_level', '-')}"
        )

        if (
            character.honor_progress is not None
            and character.honor_progress_max is not None
        ):

            self.honor_progress_label.setText(
                f"Honor Progress: "
                f"{character.honor_progress}"
                f"/"
                f"{character.honor_progress_max}"
            )

        else:

            self.honor_progress_label.setText(
                "Honor Progress: -"
            )

        def find_currency(currency_key):

            return next(
                (
                    c
                    for c in character.currencies
                    if c.currency_key == currency_key
                ),
                None,
            )

        language = get_display_language()

        coffer = find_currency(
            "restored_coffer_key"
        )

        self.coffer_keys_label.setText(
            f"{get_currency_display_name('restored_coffer_key', language)}: "
            f"{coffer.quantity if coffer else 0}"
        )

        undercoin = find_currency(
            "undercoin"
        )

        self.undercoin_label.setText(
            f"{get_currency_display_name('undercoin', language)}: "
            f"{undercoin.quantity if undercoin else 0}"
        )

        spark = find_currency(
            "radiant_spark_dust"
        )

        self.spark_label.setText(
            f"{get_currency_display_name('radiant_spark_dust', language)}: "
            f"{spark.quantity if spark else 0}"
        )

