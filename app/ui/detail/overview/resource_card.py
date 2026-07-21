from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QGridLayout,
)

from app.game_data.currency_catalog import (
    get_overview_currencies,
    get_currency_display_name,
)

from app.game_data.item_currency_catalog import (
    get_overview_item_currencies,
    get_item_currency_display_name,
)

from app.services.display_language import (
    get_display_language,
)

from app.localization.ui_strings import (
    get_ui_string,
)

from app.ui.detail.utils import (
    format_gold,
)

from app.utils.number_formatter import (
    format_number,
)


class ResourceCard(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "overviewCard"
        )

        self.setFrameShape(
            QFrame.Box
        )

        layout = QVBoxLayout(self)

        self.resources_title = QLabel()

        self.resources_title.setObjectName(
            "overviewSectionTitle"
        )

        layout.addWidget(
            self.resources_title
        )

        self.resources_grid = QGridLayout()

        layout.addLayout(
            self.resources_grid
        )

        self.resource_rows = {}

        definitions = []

        for definition in get_overview_currencies():
            definitions.append(
                ("currency", definition)
            )

        for definition in get_overview_item_currencies():
            definitions.append(
                ("item", definition)
            )

        for index, (
            kind,
            definition,
        ) in enumerate(definitions):

            name_label = QLabel()

            value_label = QLabel()

            row = index // 2

            if index % 2 == 0:

                name_column = 0
                value_column = 1

            else:

                name_column = 2
                value_column = 3

            self.resources_grid.addWidget(
                name_label,
                row,
                name_column,
            )

            self.resources_grid.addWidget(
                value_label,
                row,
                value_column,
            )

            self.resource_rows[
                (kind, definition.key)
            ] = (
                name_label,
                value_label,
            )

        self.resources_grid.setColumnStretch(
            0,
            3,
        )

        self.resources_grid.setColumnStretch(
            1,
            1,
        )

        self.resources_grid.setColumnStretch(
            2,
            3,
        )

        self.resources_grid.setColumnStretch(
            3,
            1,
        )

    def set_character(
        self,
        character,
    ):

        self.resources_title.setText(
            f"<h3>{get_ui_string('character_resources')}</h3>"
        )

        language = (
            get_display_language()
        )

        def find_currency(
            currency_key,
        ):

            return next(
                (
                    c
                    for c in character.currencies
                    if (
                        c.currency_key
                        == currency_key
                    )
                ),
                None,
            )

        for definition in (
            get_overview_currencies()
        ):

            currency = find_currency(
                definition.key
            )

            name_label, value_label = (
                self.resource_rows[
                    (
                        "currency",
                        definition.key,
                    )
                ]
            )

            name_label.setText(
                get_currency_display_name(
                    definition.key,
                    language,
                )
            )

            quantity = (
                currency.quantity
                if currency
                else 0
            )

            if definition.key == "gold":

                value_text = format_gold(
                    quantity
                )

            else:

                value_text = format_number(
                    quantity
                )

            value_label.setText(
                value_text
            )

        for definition in (
            get_overview_item_currencies()
        ):

            currency = find_currency(
                definition.key
            )

            name_label, value_label = (
                self.resource_rows[
                    (
                        "item",
                        definition.key,
                    )
                ]
            )

            name_label.setText(
                get_item_currency_display_name(
                    definition.key,
                    language,
                )
            )

            quantity = (
                currency.quantity
                if currency
                else 0
            )

            value_label.setText(
                format_number(
                    quantity
                )
            )