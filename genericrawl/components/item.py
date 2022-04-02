from copy import deepcopy

import tcod as libtcod
from .ai import BasicMonster
from ..map.dungeon_generator import CAVE_FLOOR
from .slots import SlotTypes
from ..game_messages import Message
from ..status_effect import StatusEffect


def get_throw_target(game_map, **kwargs):
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    entities = game_map.get_entities_at_tile(target_x, target_y, blocking_only=True)
    throw_target = None
    for entity in entities:
        if entity.fighter:
            throw_target = entity

    return throw_target


def equip(*args, **kwargs):
    user = args[0]
    item = args[1]

    results = user.slots.toggle_equip(item)
    equipped = results.get('equipped')
    unequipped = results.get('unequipped')

    if equipped and unequipped:
        results['use_message'] = Message('You swap out {0} for {1}.'.format(unequipped.definite_name,
                                                                            equipped.definite_name), libtcod.light_blue)
    elif equipped:
        results['use_message'] = Message('You equip {0}.'.format(equipped.definite_name), libtcod.light_blue)
    elif unequipped:
        results['use_message'] = Message('You unequip {0}.'.format(unequipped.definite_name), libtcod.light_blue)

    user.fighter.hp = min(user.fighter.hp, user.fighter.max_hp)

    return results


def throw_std(*args, **kwargs):
    item = args[1]
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    target = get_throw_target(args[2], **kwargs)

    results = {}

    if not target:
        return {'item_moved': item, 'item_x': target_x, 'item_y': target_y}

    amount = kwargs.get('amount')
    if not amount and item.equipment:
        amount = max(1, int(item.equipment.damage_bonus / 2))
    else:
        amount = 1

    results.update(target.fighter.take_damage(amount))
    results.update({'item_consumed': item})

    if amount > 0:
        results['use_message'] = Message('{0} hits {1} for {2} HP, breaking on impact.'.format(
            item.definite_name.capitalize(), target.definite_name, amount), libtcod.green)
    else:
        results['use_message'] = Message('{0} shatters harmlessly against {1}.'.format(
            item.definite_name.capitalize(), target.definite_name), libtcod.yellow)
    return results


def heal(*args, **kwargs):
    item = args[1]
    amount = kwargs.get('amount')
    throwing = kwargs.get('throwing')
    combining = kwargs.get('combining')

    if combining:
        combine_target = kwargs.get('combine_target')

        if combine_target.equipment:
            results = {}
            if combine_target.equipment.slot is SlotTypes.WEAPON:
                weapon_amount = kwargs.get('weapon_amount')
                if combine_target.equipment.enchantments.get('damage_bonus'):
                    combine_target.equipment.enchantments['damage_bonus'] += weapon_amount
                else:
                    combine_target.equipment.enchantments['damage_bonus'] = weapon_amount
                combine_target.equipment.n_enchantments -= 1
                results.update({'use_message': Message('{0} loses {1} damage.'.format(
                    combine_target.definite_name.capitalize(), abs(weapon_amount)), libtcod.red)})
            elif combine_target.equipment.slot is SlotTypes.ARMOR:
                armor_amount = kwargs.get('armor_amount')
                if combine_target.equipment.enchantments.get('max_hp_bonus'):
                    combine_target.equipment.enchantments['max_hp_bonus'] += armor_amount
                else:
                    combine_target.equipment.enchantments['max_hp_bonus'] = armor_amount
                combine_target.equipment.n_enchantments += 1
                results.update({'use_message': Message('{0} gains {1} max HP.'.format(
                    combine_target.definite_name.capitalize(), armor_amount), libtcod.green)})

            results.update({'item_consumed': item})
            return results
        else:
            return {}

    if not throwing:
        target = args[0]
    else:
        target = get_throw_target(args[2], **kwargs)
        if not target:
            target_x = kwargs.get('target_x')
            target_y = kwargs.get('target_y')
            return {'item_moved': item, 'item_x': target_x, 'item_y': target_y}

    results = {}

    player_using = target == args[0]

    if target.fighter.hp == target.fighter.max_hp:
        results['use_message'] = Message('The rune has no effect.', libtcod.yellow)
    else:
        if type(amount) is float:
            actual_amount = int(target.fighter.max_hp * amount)
        else:
            actual_amount = amount

        amount_healed = target.fighter.heal(actual_amount)
        results['item_consumed'] = item
        if player_using:
            results['use_message'] = Message('You feel rejuvenated! You recover {0} HP.'.format(amount_healed),
                                             libtcod.green)
        else:
            results['use_message'] = Message('{0} recovers {1} HP.'.format(target.definite_name.capitalize(),
                                                                           amount_healed),
                                             libtcod.red)

    return results


def pain(*args, **kwargs):
    item = args[1]
    amount = kwargs.get('amount')
    combining = kwargs.get('combining')
    throwing = kwargs.get('throwing')

    if combining:
        combine_target = kwargs.get('combine_target')
        if combine_target.equipment:
            results = {}
            if combine_target.equipment.slot is SlotTypes.WEAPON:
                weapon_amount = kwargs.get('weapon_amount')
                if combine_target.equipment.enchantments.get('damage_bonus'):
                    combine_target.equipment.enchantments['damage_bonus'] += weapon_amount
                else:
                    combine_target.equipment.enchantments['damage_bonus'] = weapon_amount
                combine_target.equipment.n_enchantments += 1
                results.update({'use_message': Message('{0} gains {1} damage.'.format(
                    combine_target.definite_name.capitalize(), weapon_amount), libtcod.green)})
            elif combine_target.equipment.slot is SlotTypes.ARMOR:
                armor_amount = kwargs.get('armor_amount')
                if combine_target.equipment.enchantments.get('max_hp_bonus'):
                    combine_target.equipment.enchantments['max_hp_bonus'] += armor_amount
                else:
                    combine_target.equipment.enchantments['max_hp_bonus'] = armor_amount
                combine_target.equipment.n_enchantments -= 1
                results.update({'use_message': Message('{0} loses {1} max HP.'.format(
                    combine_target.definite_name.capitalize(), abs(armor_amount)), libtcod.red)})

            results.update({'item_consumed': item})
            return results
        else:
            return {}

    if not throwing:
        target = args[0]
    else:
        target = get_throw_target(args[2], **kwargs)
        if not target:
            target_x = kwargs.get('target_x')
            target_y = kwargs.get('target_y')
            return {'item_moved': item, 'item_x': target_x, 'item_y': target_y}

    player_using = target == args[0]

    if type(amount) is float:
        actual_amount = int(target.fighter.max_hp * amount)
    else:
        actual_amount = amount

    results = target.fighter.take_damage(actual_amount)
    results['item_consumed'] = item
    if player_using:
        results['use_message'] = Message('You feel a searing pain! You lose {0} HP.'.format(actual_amount),
                                         libtcod.red)
    else:
        results['use_message'] = Message('{0} loses {1} HP.'.format(target.definite_name.capitalize(), actual_amount),
                                         libtcod.green)

    return results


def might(*args, **kwargs):
    item = args[1]
    amount = kwargs.get('amount')
    duration = kwargs.get('duration')
    combining = kwargs.get('combining')
    throwing = kwargs.get('throwing')

    if combining:
        combine_target = kwargs.get('combine_target')
        if combine_target.equipment and combine_target.equipment.slot is SlotTypes.WEAPON:
            weapon_amount = kwargs.get('weapon_amount')
            combine_target.equipment.n_enchantments += 1
            if combine_target.equipment.enchantments.get('attack_bonus'):
                combine_target.equipment.enchantments['attack_bonus'] += weapon_amount
            else:
                combine_target.equipment.enchantments['attack_bonus'] = weapon_amount
            return {'use_message': Message('{0} gains {1} attack.'.format(
                combine_target.definite_name.capitalize(), weapon_amount), libtcod.green), 'item_consumed': item}
        else:
            return {}

    if not throwing:
        target = args[0]
    else:
        target = get_throw_target(args[2], **kwargs)
        if not target:
            target_x = kwargs.get('target_x')
            target_y = kwargs.get('target_y')
            return {'item_moved': item, 'item_x': target_x, 'item_y': target_y}

    player_using = target == args[0]

    if type(amount) is float:
        actual_amount = int(target.fighter.attack * amount)
    else:
        actual_amount = amount

    total_amount = actual_amount
    existing_effect = target.get_status_effect('strengthened')
    if existing_effect:
        total_amount += existing_effect.properties.get('attack_bonus')
        duration += target.status_effects.get(existing_effect)
        target.status_effects.pop(existing_effect)

    target.status_effects.update({StatusEffect('strengthened', {'attack_bonus': total_amount}, None): duration})

    results = {'item_consumed': item}
    if player_using:
        results['use_message'] = Message('Your muscles grow rapidly! You gain {0} attack.'.format(actual_amount),
                                         libtcod.green)
    else:
        results['use_message'] = Message('{0} appears stronger.'.format(target.definite_name.capitalize()),
                                         libtcod.red)

    return results


def protection(*args, **kwargs):
    item = args[1]
    amount = kwargs.get('amount')
    duration = kwargs.get('duration')
    combining = kwargs.get('combining')
    throwing = kwargs.get('throwing')

    if combining:
        combine_target = kwargs.get('combine_target')
        if combine_target.equipment and combine_target.equipment.slot is SlotTypes.ARMOR:
            armor_amount = kwargs.get('armor_amount')
            combine_target.equipment.n_enchantments += 1
            if combine_target.equipment.enchantments.get('defense_bonus'):
                combine_target.equipment.enchantments['defense_bonus'] += armor_amount
            else:
                combine_target.equipment.enchantments['defense_bonus'] = armor_amount
            return {'use_message': Message('{0} gains {1} defense.'.format(
                combine_target.definite_name.capitalize(), armor_amount), libtcod.green), 'item_consumed': item}
        else:
            return {}

    if not throwing:
        target = args[0]
    else:
        target = get_throw_target(args[2], **kwargs)
        if not target:
            target_x = kwargs.get('target_x')
            target_y = kwargs.get('target_y')
            return {'item_moved': item, 'item_x': target_x, 'item_y': target_y}

    player_using = target == args[0]

    if type(amount) is float:
        actual_amount = int(target.fighter.defense * amount)
    else:
        actual_amount = amount

    total_amount = actual_amount
    existing_effect = target.get_status_effect('protected')
    if existing_effect:
        total_amount += existing_effect.properties.get('defense_bonus')
        duration += target.status_effects.get(existing_effect)
        target.status_effects.pop(existing_effect)

    target.status_effects.update({StatusEffect('protected', {'defense_bonus': total_amount}, None): duration})

    results = {'item_consumed': item}
    if player_using:
        results['use_message'] = Message('Your body feels tougher! You gain {0} defense.'.format(actual_amount),
                                         libtcod.green)
    else:
        results['use_message'] = Message('{0} appears more resilient.'.format(target.definite_name.capitalize()),
                                         libtcod.red)

    return results


def teleportation(*args, **kwargs):
    item = args[1]
    game_map = args[2]
    combining = kwargs.get('combining')
    throwing = kwargs.get('throwing')

    if combining:
        combine_target = kwargs.get('combine_target')
        x, y = game_map.find_open_tile()
        return {'use_message': Message('{0} suddenly vanishes.'.format(combine_target.definite_name.capitalize()),
                                       libtcod.yellow), 'item_consumed': item, 'move_item': combine_target,
                'target_x': x, 'target_y': y}

    if not throwing:
        target = args[0]
    else:
        target = get_throw_target(game_map, **kwargs)
        if not target:
            return {'use_message': Message('{0} suddenly vanishes.'.format(item.definite_name.capitalize()),
                                           libtcod.magenta), 'item_consumed': item}

    player_using = target == args[0]

    target.x, target.y = game_map.find_open_tile()

    results = {'item_consumed': item}
    if player_using:
        results['use_message'] = Message('Space warps around you and your surroundings suddenly change.',
                                         libtcod.magenta)
        results['recompute_fov'] = True
    else:
        results['use_message'] = Message('{0} suddenly vanishes.'.format(target.definite_name.capitalize()),
                                         libtcod.yellow)

    return results


def digging(*args, **kwargs):
    item = args[1]
    game_map = args[2]
    combining = kwargs.get('combining')
    throwing = kwargs.get('throwing')

    if combining:
        combine_target = kwargs.get('combine_target')
        return {'use_message': Message('{0} crumbles into dust.'.format(combine_target.definite_name.capitalize()),
                                       libtcod.orange), 'item_consumed': [item, combine_target]}

    if game_map.dungeon_level == 10:
        return {'use_message': Message('The ground is too hard to dig through here.', libtcod.yellow),
                'item_consumed': item}

    if not throwing:
        target = args[0]
    else:
        target = get_throw_target(game_map, **kwargs)
        if not target:
            target_x = kwargs.get('target_x')
            target_y = kwargs.get('target_y')
            for x in range(target_x - 1, target_x + 2):
                for y in range(target_y - 1, target_y + 2):
                    if game_map.contains(x, y):
                        game_map.generator.grid[x][y] = CAVE_FLOOR

            return {'use_message': Message('The walls collapse around the {0}.'.format(item.definite_name),
                                           libtcod.orange), 'item_consumed': item, 'update_fov_map': True,
                    'recompute_fov': True}

    player_using = target == args[0]

    results = {'item_consumed': item}
    if player_using:
        results['use_message'] = Message('A pit opens beneath you!', libtcod.orange)
        results['recompute_fov'] = True
        results['next_level'] = True
    else:
        results['use_message'] = Message('The ground beneath {0} collapses.'.format(target.definite_name),
                                         libtcod.orange)
        game_map.entities.remove(target)

    return results


def replication(*args, **kwargs):
    item = args[1]
    game_map = args[2]
    combining = kwargs.get('combining')
    throwing = kwargs.get('throwing')

    if combining:
        combine_target = kwargs.get('combine_target')
        player = args[0]
        player.container.items.append(deepcopy(combine_target))
        return {'use_message': Message('{0} morphs into {1}.'.format(item.definite_name.capitalize(),
                                                                     combine_target.indefinite_name), libtcod.yellow),
                'item_consumed': item}

    if not throwing:
        target = args[0]
    else:
        target = get_throw_target(game_map, **kwargs)
        if not target:
            target_x = kwargs.get('target_x')
            target_y = kwargs.get('target_y')
            return {'item_moved': item, 'item_x': target_x, 'item_y': target_y}

    player_using = target == args[0]

    results = {'item_consumed': item}
    if player_using:
        clone = deepcopy(target)
        clone.ai = BasicMonster()
        clone.ai.owner = clone
        clone.name = 'clone'
        clone.container = None
        clone.fighter.base_max_hp = clone.fighter.max_hp
        clone.fighter.base_attack = clone.fighter.attack
        clone.fighter.base_defense = clone.fighter.defense
        clone.fighter.base_damage = clone.fighter.damage
        clone.slots = None

        game_map.entities.append(clone)
        for x in range(target.x - 1, target.x + 2):
            for y in range(target.y - 1, target.y + 2):
                if game_map.is_tile_open(x, y):
                    clone.x = x
                    clone.y = y

        if clone.x != target.x or clone.y != target.y:
            results['use_message'] = Message('{0} morphs into a hostile adventurer!'.format(
                item.definite_name.capitalize()), libtcod.yellow)
        else:
            clone.x, clone.y = game_map.find_open_tile()
            results['use_message'] = Message('You feel a vague familiar presence.', libtcod.yellow)
    else:
        clone = deepcopy(target)

        game_map.entities.append(clone)
        for x in range(target.x - 1, target.x + 2):
            for y in range(target.y - 1, target.y + 2):
                if game_map.is_tile_open(x, y):
                    clone.x = x
                    clone.y = y

        if clone.x != target.x or clone.y != target.y:
            results['use_message'] = Message('{0} morphs into {1}!'.format(item.definite_name.capitalize(),
                                                                           target.indefinite_name), libtcod.yellow)
        else:
            clone.x, clone.y = game_map.find_open_tile()
            results['use_message'] = Message('You feel a vague hostile presence.', libtcod.yellow)

    return results


def cancellation(*args, **kwargs):
    item = args[1]
    game_map = args[2]
    combining = kwargs.get('combining')
    throwing = kwargs.get('throwing')

    if combining:
        combine_target = kwargs.get('combine_target')

        if combine_target.equipment and combine_target.equipment.enchantments:
            combine_target.equipment.enchantments = {}
            combine_target.equipment.n_enchantments = 0
            return {'use_message': Message('The glow of enchantment fades from {0}.'.format(
                combine_target.definite_name), libtcod.yellow), 'item_consumed': item}

        return {}

    if not throwing:
        target = args[0]
    else:
        target = get_throw_target(game_map, **kwargs)
        if not target:
            target_x = kwargs.get('target_x')
            target_y = kwargs.get('target_y')
            return {'item_moved': item, 'item_x': target_x, 'item_y': target_y}

    player_using = target == args[0]
    if target.status_effects:
        target.status_effects = {}

        results = {'item_consumed': item}
        if player_using:
            results['use_message'] = Message('You feel normal again.', libtcod.yellow)
        else:
            results['use_message'] = Message('{0} returns to normal.'.format(target.definite_name.capitalize()),
                                             libtcod.yellow)
    else:
        results = {'item_consumed': item, 'use_message': Message('{0} has no effect.'.format(
            item.definite_name.capitalize()), libtcod.yellow)}

    return results


class Item:
    def __init__(self, use_function=None, combine_function=None, throw_function=throw_std, **kwargs):
        self.use_function = use_function
        self.combine_function = combine_function
        self.throw_function = throw_function
        self.function_kwargs = kwargs

    def use(self, user, game_map, **kwargs):
        kwargs.update(self.function_kwargs)

        if kwargs.get('combining') and self.combine_function:
            return self.combine_function(user, self.owner, game_map, **kwargs)
        elif kwargs.get('throwing') and self.throw_function:
            return self.throw_function(user, self.owner, game_map, **kwargs)
        elif self.use_function:
            return self.use_function(user, self.owner, game_map, **kwargs)

        return {'use_message': Message('{0} cannot be used'.format(self.owner.definite_name.capitalize()),
                                         libtcod.yellow)}
