# Represents a single reputation entry.


class Reputation:

    def __init__(
        self,
        name,
        rep_type,
        level=None,
        current=None,
        maximum=None,
    ):
        self.name = name
        self.rep_type = rep_type
        self.level = level
        self.current = current
        self.maximum = maximum