from random import randint

import libtcodpy as libtcod
from game_messages import Message


def get_throw_target(target_x, target_y, game_map):
    entities = game_map.get_entities_at_tile(target_x, target_y, blocking_only=True)
    throw_target = None
    for entity in entities:
        if entity.fighter:
            throw_target = entity

    return throw_target


def heal(*args, **kwargs):
    item = args[1]
    amount = kwargs.get('amount')
    throwing = kwargs.get('throwing')

    if not throwing:
        entity = args[0]
    else:
        item = args[1]
        target_x = kwargs.get('target_x')
        target_y = kwargs.get('target_y')
        game_map = kwargs.get('game_map')

        entity = get_throw_target(target_x, target_y, game_map)

        if not entity:
            return {'item_moved': item, 'item_x': target_x, 'item_y': target_y}

    results = {}

    player_using = entity == args[0]

    if entity.fighter.hp == entity.fighter.max_hp:
        if player_using:
            results['use_message'] = Message('You are already fully healed.', libtcod.yellow)
        else:
            results['item_consumed'] = item
            results['use_message'] = Message('The rune has no effect on {0}.'.format(entity.definite_name()),
                                             libtcod.yellow)
    else:
        amount_healed = entity.fighter.heal(amount)
        results['item_consumed'] = item
        if player_using:
            results['use_message'] = Message('You recover {0} HP.'.format(amount_healed), libtcod.green)
        else:
            results['use_message'] = Message('{0} recovers {1} HP.'.format(entity.definite_name(), amount_healed),
                                             libtcod.green)

    return results


def throw_std(*args, **kwargs):
    item = args[1]
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    game_map = kwargs.get('game_map')

    target_entity = get_throw_target(target_x, target_y, game_map)

    if not target_entity:
        return {'item_moved': item, 'item_x': target_x, 'item_y': target_y}

    throw_damage = kwargs.get('throw_damage')
    if not throw_damage:
        throw_damage = randint(1, 4)

    results = target_entity.fighter.damage(throw_damage)
    if results.get('damage') > 0:
        results['use_message'] = Message('{0} hits {1} for {2} HP.'.format(item.definite_name(),
                                                                           target_entity.definite_name(),
                                                                           results['damage']))
    else:
        results['use_message'] = Message('{0} bounces off {1} harmlessly.'.format(item.definite_name(),
                                                                                  target_entity.definite_name()))
    return results


class Item:
    def __init__(self, use_function=None, throw_function=throw_std, **kwargs):
        self.use_function = use_function
        self.throw_function = throw_function
        self.function_kwargs = kwargs

    def use(self, user, **kwargs):
        results = {}

        if kwargs.get('throwing'):
            kwargs = {**self.function_kwargs, **kwargs}
            throw_results = self.throw_function(user, self.owner, **kwargs)
            results = {**results, **throw_results}
        elif self.use_function is None:
            results['use_message'] = Message('{0} cannot be used'.format(self.owner.definite_name().capitalize()),
                                             libtcod.yellow)
            return results
        else:
            kwargs = {**self.function_kwargs, **kwargs}
            item_use_results = self.use_function(user, self.owner, **kwargs)
            results = {**results, **item_use_results}

        return results
