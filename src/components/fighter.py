from game_messages import Message


class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = max(0, defense)
        self.power = max(0, power)

    def attack(self, target):
        results = {}

        damage_results = target.damage(self.power)
        damage = damage_results.get('damage')

        if damage > 0:
            results['attack_message'] = Message('{0} attacks {1} for {2} HP.'.format(
                self.owner.definite_name().capitalize(), target.owner.definite_name(), damage))

            results = {**results, **damage_results}
        else:
            results['attack_message'] = Message(
                '{0} attacks {1} but does no damage.'.format(self.owner.definite_name().capitalize(),
                                                             target.owner.definite_name()))

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
