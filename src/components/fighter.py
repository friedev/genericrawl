from game_messages import Message


class Fighter:
    def __init__(self, hp, defense, attack):
        self.base_max_hp = hp
        self.base_defense = max(0, defense)
        self.base_attack = max(0, attack)
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

    def attack_entity(self, target):
        results = {}

        damage_results = target.damage(self.attack)
        damage = damage_results.get('damage')

        if damage > 0:
            results['attack_message'] = Message('{0} attacks {1} for {2} HP.'.format(
                self.owner.definite_name.capitalize(), target.owner.definite_name, damage))

            results = {**results, **damage_results}
        else:
            results['attack_message'] = Message(
                '{0} attacks {1} but does no damage.'.format(self.owner.definite_name.capitalize(),
                                                             target.owner.definite_name))

        return results

    def damage(self, amount, ignore_defense=False):
        if ignore_defense:
            actual_amount = amount
        else:
            actual_amount = int(amount - self.defense)
        self.hp = max(self.hp - actual_amount, 0)

        results = {'damage': actual_amount}
        if self.hp == 0:
            results['dead'] = [self.owner]
        return results

    def heal(self, amount):
        actual_amount = min(self.max_hp - self.hp, amount)
        self.hp = self.hp + actual_amount
        return actual_amount
