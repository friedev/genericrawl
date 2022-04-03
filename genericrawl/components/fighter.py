from random import random, getrandbits, randint

import tcod

from ..game_messages import Message


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


def calc_damage(damage):
    max_variation = max(1, int(damage / 4))
    variation = randint(-max_variation, max_variation)
    return max(1, damage + variation)


class Fighter:
    def __init__(self, hp, defense, attack, damage):
        self.base_max_hp = hp
        self.base_defense = max(0, defense)
        self.base_attack = max(0, attack)
        self.base_damage = max(1, damage)
        self.hp = hp

    @property
    def max_hp(self):
        bonus = 0

        if self.owner.slots:
            bonus += self.owner.slots.max_hp_bonus

        return self.base_max_hp + bonus

    @property
    def attack(self):
        bonus = 0

        if self.owner.slots:
            bonus += self.owner.slots.attack_bonus

        for effect in self.owner.status_effects:
            attack_bonus = effect.properties.get("attack_bonus")
            if attack_bonus:
                bonus += attack_bonus

        return self.base_attack + bonus

    @property
    def defense(self):
        bonus = 0

        if self.owner.slots:
            bonus += self.owner.slots.defense_bonus

        for effect in self.owner.status_effects:
            defense_bonus = effect.properties.get("defense_bonus")
            if defense_bonus:
                bonus += defense_bonus

        return self.base_defense + bonus

    @property
    def damage(self):
        bonus = 0

        if self.owner.slots:
            bonus += self.owner.slots.damage_bonus

        for effect in self.owner.status_effects:
            damage_bonus = effect.properties.get("damage_bonus")
            if damage_bonus:
                bonus += damage_bonus

        return self.base_damage + bonus

    def attack_entity(self, target, is_player=False, target_is_player=False):
        attack_hit = calc_hit_chance(self.attack, target.defense)

        if not attack_hit:
            return {
                "attack_message": Message(
                    "{0} blocks {1}'s attack.".format(
                        target.owner.definite_name.capitalize(),
                        self.owner.definite_name,
                    ),
                    tcod.light_gray,
                )
            }

        if self.damage <= 0:
            return {
                "attack_message": Message(
                    "{0} attacks {1} but does no damage.".format(
                        self.owner.definite_name.capitalize(),
                        target.owner.definite_name,
                    ),
                    tcod.light_gray,
                )
            }

        results = target.take_damage(self.damage)

        if is_player:
            color = tcod.green
        elif target_is_player:
            color = tcod.red
        else:
            color = tcod.white

        results["attack_message"] = Message(
            "{0} attacks {1} for {2} HP.".format(
                self.owner.definite_name.capitalize(),
                target.owner.definite_name,
                results.get("damage"),
            ),
            color,
        )

        return results

    def take_damage(self, amount, randomize=True):
        if randomize:
            amount = calc_damage(amount)
        results = {"damage": amount}

        self.hp = max(self.hp - amount, 0)

        if self.hp == 0:
            results["dead"] = [self.owner]

        return results

    def heal(self, amount):
        actual_amount = min(self.max_hp - self.hp, amount)
        self.hp = self.hp + actual_amount
        return actual_amount
