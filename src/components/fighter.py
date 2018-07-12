from game_messages import Message


class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = max(1, defense)
        self.power = max(0, power)

    def attack(self, target):
        damage = max(0, self.power - target.defense)

        results = {}

        if damage > 0:
            target.hp = max(target.hp - damage, 0)
            results['message'] = Message('{0} attacks {1} for {2} hit point{3}.'.format(
                self.owner.definite_name().capitalize(),
                target.owner.definite_name(), str(damage),
                's' if damage > 1 else ''))

            if target.hp == 0:
                results['dead'] = [target.owner]
        else:
            results['message'] = Message(
                '{0} attacks {1} but does no damage.'.format(self.owner.definite_name().capitalize(),
                                                             target.owner.definite_name()))

        return results
