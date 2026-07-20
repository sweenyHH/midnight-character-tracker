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

        # Mythic+   
        self.mythic_score = None

        # PvP
        self.honor_level = None
        self.honor_progress = None
        self.honor_progress_max = None
      

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
            "row3": [],
        }

    def add_currency(self, currency):
        self.currencies.append(currency)

    def add_equipment(self, item):
        self.equipment.append(item)

