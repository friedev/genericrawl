from enum import Enum

from components.ai import BasicMonster
from components.equipment import Equipment
from components.fighter import Fighter
from components.item import *
from components.sight import Sight
from components.slots import SlotTypes
from entity import Entity
from render import RenderOrder


def create_enemy(char, color, name, hp, defense, attack, damage, is_name_proper=False, fov_radius=8):
    return Entity(0, 0, char, color, name, is_name_proper=is_name_proper, render_order=RenderOrder.ENEMY,
                  components={'sight': Sight(fov_radius),
                              'fighter': Fighter(hp, defense, attack, damage),
                              'ai': BasicMonster()})


def create_weapon(name, attack, damage, char=')', color=libtcod.lighter_gray, is_name_proper=False):
    return Entity(0, 0, char, color, name, is_name_proper=is_name_proper, blocks=False, render_order=RenderOrder.ITEM,
                  components={'item': Item(use_function=equip),
                              'equipment': Equipment(SlotTypes.WEAPON, attack_bonus=attack, damage_bonus=damage)})


def create_armor(name, defense, max_hp, char='[', color=libtcod.lighter_gray, is_name_proper=False):
    return Entity(0, 0, char, color, name, is_name_proper=is_name_proper, blocks=False, render_order=RenderOrder.ITEM,
                  components={'item': Item(use_function=equip),
                              'equipment': Equipment(SlotTypes.ARMOR, defense_bonus=defense, max_hp_bonus=max_hp)})


def create_rune(color, name, rune_function, char='*', is_name_proper=False, combine_function=None, throw_function=None,
                **kwargs):
    if not combine_function:
        combine_function = rune_function
    if not throw_function:
        throw_function = rune_function
    return Entity(0, 0, char, color, name, is_name_proper=is_name_proper, blocks=False, render_order=RenderOrder.ITEM,
                  components={'item': Item(rune_function, combine_function, throw_function, **kwargs)})


class EntityTemplates(Enum):
    # Enemies
    GOBLIN = create_enemy('g', libtcod.darker_green, 'goblin', hp=5, defense=0, attack=1, damage=1)
    ORC = create_enemy('o', libtcod.green, 'orc', hp=8, defense=1, attack=1, damage=2)
    OGRE = create_enemy('O', libtcod.darker_green, 'ogre', hp=16, defense=3, attack=3, damage=4)
    TROLL = create_enemy('T', libtcod.darker_gray, 'troll', hp=24, defense=7, attack=5, damage=8)

    # Weapons
    DAGGER = create_weapon('dagger', attack=1, damage=2)
    SHORTSWORD = create_weapon('shortsword', attack=3, damage=6)
    ARMING_SWORD = create_weapon('arming sword', attack=5, damage=10)
    LONGSWORD = create_weapon('longsword', attack=7, damage=14)

    # Armor
    GAMBESON = create_armor('gambeson', defense=1, max_hp=5, color=libtcod.lighter_sepia)
    LEATHER_CUIRASS = create_armor('leather cuirass', defense=3, max_hp=15, color=libtcod.sepia)
    CHAIN_HAUBERK = create_armor('chain hauberk', defense=5, max_hp=25)
    PLATE_ARMOR = create_armor('plate armor', defense=7, max_hp=35)

    # Runes
    ROCK = create_rune(libtcod.darker_gray, 'rock', None, throw_function=throw_std)
    RUNE_HEALING = create_rune(libtcod.darker_green, 'rune of healing', heal, amount=0.5, weapon_amount=-2,
                               armor_amount=5)
    RUNE_PAIN = create_rune(libtcod.red, 'rune of pain', pain, amount=0.5, weapon_amount=2, armor_amount=-5)
    RUNE_MIGHT = create_rune(libtcod.yellow, 'rune of might', might, amount=3, duration=10, weapon_amount=1)
    RUNE_PROTECTION = create_rune(libtcod.blue, 'rune of protection', protection, amount=3, duration=10, armor_amount=1)
    RUNE_TELEPORTATION = create_rune(libtcod.magenta, 'rune of teleportation', teleportation)


def weight_range(value, start, end):
    weights = []
    for i in range(0, end + 2):
        if i in range(start, end):
            weights.append(value)
        else:
            weights.append(0)

    return weights


ENEMY_WEIGHTS = {
    EntityTemplates.GOBLIN: [1, 3, 1, 1, 0],
    EntityTemplates.ORC:    [0, 2, 3, 2, 2, 1, 0],
    EntityTemplates.OGRE:   [0, 0, 0, 1],
    EntityTemplates.TROLL:  [0, 0, 0, 0, 1, 1, 2]
}

ITEM_WEIGHTS = {
    EntityTemplates.DAGGER: weight_range(1, 0, 1),
    EntityTemplates.SHORTSWORD: weight_range(1, 2, 3),
    EntityTemplates.ARMING_SWORD: weight_range(1, 4, 5),
    EntityTemplates.LONGSWORD: weight_range(1, 6, 7),

    EntityTemplates.GAMBESON: weight_range(1, 0, 1),
    EntityTemplates.LEATHER_CUIRASS: weight_range(1, 2, 3),
    EntityTemplates.CHAIN_HAUBERK: weight_range(1, 4, 5),
    EntityTemplates.PLATE_ARMOR: weight_range(1, 6, 7),

    EntityTemplates.ROCK: [2],
    EntityTemplates.RUNE_HEALING: [4],
    EntityTemplates.RUNE_PAIN: [2],
    EntityTemplates.RUNE_MIGHT: [1],
    EntityTemplates.RUNE_PROTECTION: [1],
    EntityTemplates.RUNE_TELEPORTATION: [1]
}


def weighted_choice(weights):
    weight_list = list(weights.values())
    selection = randint(1, sum(weight_list))

    weight_index = 0
    choice_index = 0
    for weight in weight_list:
        weight_index += weight

        if selection <= weight_index:
            break

        choice_index += 1

    return list(weights.keys())[choice_index]


def get_weights_for_level(weights, dungeon_level):
    level_weights = weights.copy()
    for key in weights.keys():
        weight = weights[key]
        if len(weight) > dungeon_level - 1:
            level_weights[key] = weight[dungeon_level - 1]
        else:
            level_weights[key] = weight[len(weight) - 1]
    return level_weights
