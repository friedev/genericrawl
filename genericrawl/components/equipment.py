class Equipment:
    def __init__(self, slot, tier=1, max_hp_bonus=0, attack_bonus=0, defense_bonus=0, damage_bonus=0, enchantments={},
                 n_enchantments=0):
        self.slot = slot
        self.tier = tier
        self.base_max_hp_bonus = max_hp_bonus
        self.base_attack_bonus = attack_bonus
        self.base_defense_bonus = defense_bonus
        self.base_damage_bonus = damage_bonus
        self.enchantments = enchantments
        self.n_enchantments = n_enchantments

    @property
    def max_hp_bonus(self):
        bonus = 0

        enchantment = self.enchantments.get('max_hp_bonus')
        if enchantment:
            bonus += enchantment

        return self.base_max_hp_bonus + bonus

    @property
    def attack_bonus(self):
        bonus = 0

        enchantment = self.enchantments.get('attack_bonus')
        if enchantment:
            bonus += enchantment

        return self.base_attack_bonus + bonus

    @property
    def defense_bonus(self):
        bonus = 0

        enchantment = self.enchantments.get('defense_bonus')
        if enchantment:
            bonus += enchantment

        return self.base_defense_bonus + bonus

    @property
    def damage_bonus(self):
        bonus = 0

        enchantment = self.enchantments.get('damage_bonus')
        if enchantment:
            bonus += enchantment

        return self.base_damage_bonus + bonus
