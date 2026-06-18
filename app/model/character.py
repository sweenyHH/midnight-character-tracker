
# Defines the core data structures for characters and currencies.

class Currency:
 
#    Represents a single currency entry parsed from the file.

    def __init__(self, name, quantity=0, max_value=None, category="Unknown"):
        self.name = name
        self.quantity = quantity
        self.max_value = max_value
        self.category = category


class Character:

#    Represents a single character with its parsed data.

    def __init__(self, name):
        self.name = name
        self.location = {}
        self.currencies = []

    def add_currency(self, currency):
        self.currencies.append(currency)


class Reputation:

# Represents a single reputation entry

    def __init__(self, name, rep_type, level=None, current=None, maximum=None):
        self.name = name              # e.g. "Amani Tribe"
        self.rep_type = rep_type      # "renown" or "standard"
        self.level = level            # "Neutral" OR integer for renown
        self.current = current        # current progress
        self.maximum = maximum        # max progress