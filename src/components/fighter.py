import libtcodpy as libtcod
from random import random, getrandbits

from game_messages import Message


def calc_hit_chance(attack, defense):
    if attack <= 0:
        if defense <= 0:
            return bool(getrandbits(1))
        else:
            return False

    if defense <= 0:
        return True

    chance = attack / defense / 2
    clamped_chance = max(0, min(1, chance))
    return random() < clamped_chance


class Fighter:
    def __init__(self, hp, defense, attack, damage):
        self.base_max_hp = hp
        self.base_defense = max(0, defense)
        self.base_attack = max(0, attack)
        self.base_damage = max(1, damage)
        self.hp = hp

    @property
    def max_hp(self):
        if self.owner and self.owner.slots:
            bonus = self.owner.slots.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def attack(self):
        if self.owner and self.owner.slots:
            bonus = self.owner.slots.attack_bonus
        else:
            bonus = 0

        return self.base_attack + bonus

    @property
    def defense(self):
        if self.owner and self.owner.slots:
            bonus = self.owner.slots.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    @property
    def damage(self):
        if self.owner and self.owner.slots:
            bonus = self.owner.slots.damage_bonus
        else:
            bonus = 0

        return self.base_damage + bonus

    def attack_entity(self, target):
        attack_hit = calc_hit_chance(self.attack, target.defense)

        if not attack_hit:
            return {'attack_message': Message('{0} misses {1}.'.format(self.owner.definite_name.capitalize(),
                                                                       target.owner.definite_name), libtcod.light_gray)}

        if self.damage <= 0:
            return {'attack_message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.definite_name.capitalize(), target.owner.definite_name))}

        results = target.take_damage(self.damage)

        results['attack_message'] = Message('{0} attacks {1} for {2} HP.'.format(
            self.owner.definite_name.capitalize(), target.owner.definite_name, self.damage))

        return results

    def take_damage(self, amount):
        self.hp = max(self.hp - amount, 0)

        if self.hp == 0:
            return {'dead': [self.owner]}

        return {}

    def heal(self, amount):
        actual_amount = min(self.max_hp - self.hp, amount)
        self.hp = self.hp + actual_amount
        return actual_amount
