from enum import Enum, auto


class SlotTypes(Enum):
    WEAPON = auto()
    ARMOR = auto()


class Slots:
    def __init__(self, slot_dict=None):
        if slot_dict:
            self.slot_dict = slot_dict
        else:
            self.slot_dict = {}
            for slot_type in SlotTypes:
                self.slot_dict[slot_type] = None

    @property
    def max_hp_bonus(self):
        bonus = 0

        for item in self.slot_dict.values():
            if item:
                bonus += item.equipment.max_hp_bonus

        return bonus

    @property
    def attack_bonus(self):
        bonus = 0

        for item in self.slot_dict.values():
            if item:
                bonus += item.equipment.attack_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        for item in self.slot_dict.values():
            if item:
                bonus += item.equipment.defense_bonus

        return bonus

    @property
    def damage_bonus(self):
        bonus = 0

        for item in self.slot_dict.values():
            if item:
                bonus += item.equipment.damage_bonus

        return bonus


    def toggle_equip(self, item):
        if not item.equipment:
            return False

        results = {}

        slot = item.equipment.slot
        equipped = self.slot_dict.get(slot)

        if equipped:
            if equipped is item:
                self.slot_dict[slot] = None
                results['unequipped'] = item
            else:
                results['unequipped'] = equipped
                self.slot_dict[slot] = item
                results['equipped'] = item
        else:
            self.slot_dict[slot] = item
            results['equipped'] = item

        return results

    def is_equipped(self, item):
        if not item.equipment:
            return False
        return item is self.slot_dict.get(item.equipment.slot)
