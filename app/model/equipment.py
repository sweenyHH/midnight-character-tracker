# Represents a single equipment item.


class Equipment:

    def __init__(
        self,
        slot,
        name,
        item_level=None,
        item_type=None,
        enchanted=False,
        quality=None,
    ):
        self.slot = slot
        self.name = name
        self.item_level = item_level
        self.item_type = item_type
        self.enchanted = enchanted
        self.quality = quality