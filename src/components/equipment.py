class Equipment:
    def __init__(self, slot, max_hp_bonus=0, attack_bonus=0, defense_bonus=0, damage_bonus=0):
        self.slot = slot
        self.max_hp_bonus = max_hp_bonus
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.damage_bonus = damage_bonus
