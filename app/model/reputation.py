# Represents a single reputation entry.


class Reputation:

    def __init__(
        self,
        name,
        rep_type,

        level=None,
        current=None,
        maximum=None,

        reputation_id=None,
        reputation_key=None,
    ):
        self.name = name
        self.rep_type = rep_type

        self.level = level
        self.current = current
        self.maximum = maximum

        self.reputation_id = reputation_id
        self.reputation_key = reputation_key