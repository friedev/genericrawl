import libtcodpy as libtcod
from game_messages import Message


class Item:
    def __init__(self, use_function=None, **kwargs):
        self.use_function = use_function
        self.function_kwargs = kwargs

    def use(self, user, **kwargs):
        results = {}

        if self.use_function is None:
            results['use_message'] = Message('{0} cannot be used'.format(self.owner.definite_name().capitalize()),
                                                   libtcod.yellow)
        else:
            kwargs = {**self.function_kwargs, **kwargs}
            item_use_results = self.use_function(user, **kwargs)
            results = {**results, **item_use_results}
            if results.get('item_consumed'):
                results['item_consumed'] = self.owner

        return results


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = {}

    if entity.fighter.hp == entity.fighter.max_hp:
        results['use_message'] = Message('You are already fully healed.', libtcod.yellow)
    else:
        amount_healed = entity.fighter.heal(amount)
        results['item_consumed'] = True
        results['use_message'] = Message('You recover {0} HP.'.format(amount_healed), libtcod.green)

    return results
