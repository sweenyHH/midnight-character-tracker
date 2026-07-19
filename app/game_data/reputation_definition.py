
class ReputationDefinition:

    def __init__(
        self,
        faction_id,
        key,

        english_name,
        german_name,
        french_name,

        warband_wide=False,
        deprecated=False,
        featured=False,
    ):
        self.faction_id = faction_id
        self.key = key

        self.english_name = english_name
        self.german_name = german_name
        self.french_name = french_name

        self.warband_wide = warband_wide
        self.deprecated = deprecated
        self.featured = featured