# Defines the core data structures for characters, reputations and currencies.

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
        self.equipment = []

# Vault progress
        
        self.vault = {
            "row1": [],
            "row2": [],
            "row3": []
        }


    def add_currency(self, currency):
        self.currencies.append(currency)

    
    def add_equipment(self, item):
        self.equipment.append(item)



# Represents a single reputation entry

class Reputation:

    def __init__(self, name, rep_type, level=None, current=None, maximum=None):
        self.name = name              # e.g. "Amani Tribe"
        self.rep_type = rep_type      # "renown" or "standard"
        self.level = level            # "Neutral" OR integer for renown
        self.current = current        # current progress
        self.maximum = maximum        # max progress

# Represents a single equipment item

class Equipment:

    def __init__(
        self,
        slot,
        name,
        item_level=None,
        item_type=None,
        enchanted=False,
        quality=None  
    ):
        self.slot = slot
        self.name = name
        self.item_level = item_level
        self.item_type = item_type
        self.enchanted = enchanted
        self.quality = quality
