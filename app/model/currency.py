# Represents a single currency entry parsed from the file.


class Currency:

    def __init__(
        self,
        name,
        quantity,
        max_total=None,
        weekly_current=None,
        weekly_max=None,
        currency_id=None,
        currency_type=None,
    ):
        self.name = name
        self.quantity = quantity

        self.max_total = max_total
        self.weekly_current = weekly_current
        self.weekly_max = weekly_max

        self.currency_id = currency_id
        self.currency_type = currency_type

        self.groups = []
        self.category = None

    @property
    def has_total_cap(self):
        return self.max_total is not None

    @property
    def has_weekly_cap(self):
        return self.weekly_max is not None