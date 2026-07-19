class ItemCurrencyDefinition:

    def __init__(
        self,
        item_id,
        key,

        english_name,
        german_name,
        french_name,

        featured=False,
    ):
        self.item_id = item_id
        self.key = key

        self.english_name = english_name
        self.german_name = german_name
        self.french_name = french_name

        self.featured = featured