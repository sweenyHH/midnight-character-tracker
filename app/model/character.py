# Defines the core data structures for characters and currencies.

# Represents a single currency entry parsed from the file.

class Currency:
 
    def __init__(
        self,
        name,
        quantity,
        max_total=None,
        weekly_current=None,
        weekly_max=None,
    ):
        self.name = name
        self.quantity = quantity
        self.max_total = max_total
        self.weekly_current = weekly_current
        self.weekly_max = weekly_max
        self.groups = []     
        self.category = None 


# Helper properties

    @property
    def has_total_cap(self):
        return self.max_total is not None

    @property
    def has_weekly_cap(self):
        return self.weekly_max is not None

# Represents a single character with its parsed data.


class Character:
    def __init__(self, name: str):
        self.name = name
        self.source_file = None

        # Identity
        self.faction = None
        self.race = None
        self.character_class = None
        self.specialization = None
        self.level = None

        # Location
        self.zone = None
        self.subzone = None
        self.map = None
        self.map_id = None
        self.parent_map = None
        self.parent_map_id = None
        self.coordinates = None
        self.hearthstone_location = None

        # Stats
        self.primary_stat = None
        self.health = None
        self.armor = None

        # Item levels
        self.avg_item_level = None
        self.equipped_item_level = None
        self.pvp_item_level = None

        # XP
        self.xp = None
        self.xp_to_level = None
        self.xp_progress = None

        # Flexible data
        self.attributes = {}
        self.combat_ratings = {}

        # Collections
        self.currencies = []
        self.reputations = []

        # Vault progress
        
        self.vault = {
            "row1": [],
            "row2": [],
            "row3": []
        }


    def add_currency(self, currency):
        self.currencies.append(currency)


# Represents a single reputation entry

class Reputation:

    def __init__(self, name, rep_type, level=None, current=None, maximum=None):
        self.name = name              # e.g. "Amani Tribe"
        self.rep_type = rep_type      # "renown" or "standard"
        self.level = level            # "Neutral" OR integer for renown
        self.current = current        # current progress
        self.maximum = maximum        # max progress