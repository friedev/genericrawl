# def boost_stat(*args, **kwargs):
#     entity = args[0]
#     apply = kwargs.get('apply')
#     stat = kwargs.get('stat')
#     amount = kwargs.get('amount')
#
#     if not apply:
#         amount = -amount
#
#     if stat == 'attack':
#         entity.fighter.base_attack += amount
#     elif stat == 'defense':
#         entity.fighter.base_defense += amount
#     elif stat == 'damage':
#         entity.fighter.base_damage += amount


def damage(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get("amount")

    return entity.fighter.take_damage(amount)


class StatusEffect:
    def __init__(
        self,
        name,
        properties,
        effect_function,
        continuous=True,
        hidden=False,
        **kwargs,
    ):
        self.name = name
        self.properties = properties
        self.effect_function = effect_function
        self.continuous = continuous
        self.hidden = hidden
        self.applied = False
        self.kwargs = kwargs

    def apply(self, entity):
        if self.effect_function and (self.continuous or not self.applied):
            return self.effect_function(entity, apply=True, **self.kwargs)
        return {}

    def stop(self, entity):
        if self.effect_function:
            return self.effect_function(entity, apply=False, **self.kwargs)
        return {}
