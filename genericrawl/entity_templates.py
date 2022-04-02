from enum import Enum
from random import randint

from .components.ai import BasicMonster
from .components.equipment import Equipment
from .components.fighter import Fighter
from .components.item import *
from .components.sight import Sight
from .components.slots import SlotTypes
from .entity import Entity
from .render import RenderOrder


def create_enemy(char, color, name, hp, defense, attack, damage, is_name_proper=False, fov_radius=8):
    return Entity(0, 0, char, color, name, is_name_proper=is_name_proper, render_order=RenderOrder.ENEMY,
                  components={'sight': Sight(fov_radius),
                              'fighter': Fighter(hp, defense, attack, damage),
                              'ai': BasicMonster()})


def create_sword(name, tier, attack, damage, is_name_proper=False):
    return create_weapon('/', libtcod.lighter_gray, name, tier, attack, damage, is_name_proper)


def create_polearm(name, tier, attack, damage, is_name_proper=False):
    return create_weapon('|', libtcod.darker_orange, name, tier, attack, damage, is_name_proper)


def create_heavy(name, tier, attack, damage, is_name_proper=False):
    return create_weapon('(', libtcod.dark_gray, name, tier, attack, damage, is_name_proper)


def create_weapon(char, color, name, tier, attack, damage, is_name_proper=False):
    return Entity(0, 0, char, color, name, is_name_proper=is_name_proper, blocks=False, render_order=RenderOrder.ITEM,
                  components={'item': Item(use_function=equip),
                              'equipment': Equipment(SlotTypes.WEAPON, tier=tier, attack_bonus=attack,
                                                     damage_bonus=damage)})


def create_def_armor(name, tier, defense, hp, is_name_proper=False):
    return create_armor('}', libtcod.lighter_gray, name, tier, defense, hp, is_name_proper)


def create_hp_armor(name, tier, defense, hp, is_name_proper=False):
    return create_armor('[', libtcod.darker_orange, name, tier, defense, hp, is_name_proper)


def create_armor(char, color, name, tier, defense, hp, is_name_proper=False):
    return Entity(0, 0, char, color, name, is_name_proper=is_name_proper, blocks=False, render_order=RenderOrder.ITEM,
                  components={'item': Item(use_function=equip),
                              'equipment': Equipment(SlotTypes.ARMOR, tier=tier, defense_bonus=defense,
                                                     max_hp_bonus=hp)})


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
    GOBLIN = create_enemy('g', libtcod.darker_green, 'goblin',      hp=6,  attack=2,  defense=1,  damage=2)
    KOBOLD = create_enemy('k', libtcod.light_pink, 'kobold',        hp=7,  attack=1,  defense=0,  damage=1)
    ZOMBIE = create_enemy('z', libtcod.green, 'zombie',             hp=10, attack=1,  defense=2,  damage=1)
    ORC = create_enemy('o', libtcod.green, 'orc',                   hp=15, attack=3,  defense=3,  damage=4)
    GNOLL = create_enemy('G', libtcod.dark_orange, 'gnoll',         hp=22, attack=4,  defense=6,  damage=5)
    SKELETON = create_enemy('s', libtcod.white, 'skeleton',         hp=24, attack=2,  defense=5,  damage=3)
    SPIDER = create_enemy('S', libtcod.darker_gray, 'spider',       hp=28, attack=8,  defense=5,  damage=9)
    WEREWOLF = create_enemy('w', libtcod.darker_gray, 'werewolf',   hp=26, attack=6,  defense=5,  damage=6)
    OGRE = create_enemy('O', libtcod.darker_green, 'ogre',          hp=50, attack=4,  defense=7,  damage=8)
    WYVERN = create_enemy('W', libtcod.red, 'wyvern',               hp=45, attack=13, defense=7,  damage=14)
    CYCLOPS = create_enemy('C', libtcod.dark_orange, 'cyclops',     hp=55, attack=9,  defense=10, damage=12)
    TROLL = create_enemy('T', libtcod.darker_gray, 'troll',         hp=60, attack=7,  defense=12, damage=10)
    HYDRA = create_enemy('H', libtcod.dark_cyan, 'hydra',           hp=50, attack=18, defense=9,  damage=20)
    MINOTAUR = create_enemy('M', libtcod.darker_orange, 'minotaur', hp=60, attack=12, defense=12, damage=18)
    DRAGON = create_enemy('D', libtcod.red, 'dragon',               hp=80, attack=10, defense=20, damage=15)

    # Weapons
    DAGGER = create_sword('dagger',               tier=1, attack=3,  damage=2)
    SPEAR = create_polearm('spear',               tier=1, attack=2,  damage=3)
    CLUB = create_heavy('club',                   tier=1, attack=1,  damage=6)
    SHORTSWORD = create_sword('shortsword',       tier=3, attack=6,  damage=4)
    PIKE = create_polearm('pike',                 tier=3, attack=4,  damage=6)
    MACE = create_heavy('mace',                   tier=3, attack=3,  damage=10)
    ARMING_SWORD = create_sword('arming sword',   tier=5, attack=9,  damage=6)
    POLEAXE = create_polearm('poleaxe',           tier=5, attack=7,  damage=8)
    WARHAMMER = create_heavy('warhammer',         tier=5, attack=5,  damage=14)
    BASTARD_SWORD = create_sword('bastard sword', tier=7, attack=12, damage=8)
    HALBERD = create_polearm('halberd',           tier=7, attack=9,  damage=12)
    MORNING_STAR = create_heavy('morning star',   tier=7, attack=7,  damage=18)
    LONGSWORD = create_sword('longsword',         tier=9, attack=15, damage=10)
    GLAIVE = create_polearm('glaive',             tier=9, attack=12, damage=14)
    BATTLE_AXE = create_heavy('battle axe',       tier=9, attack=9,  damage=22)

    # Armor
    LIGHT_HAUBERK = create_def_armor('light hauberk',     tier=2, defense=3,  hp=10)
    GAMBESON = create_hp_armor('gambeson',                tier=2, defense=2,  hp=15)
    FULL_HAUBERK = create_def_armor('full hauberk',       tier=4, defense=6,  hp=20)
    LEATHER_CUIRASS = create_hp_armor('leather cuirass',  tier=4, defense=4,  hp=30)
    REINFORCED_MAIL = create_def_armor('reinforced mail', tier=6, defense=9,  hp=30)
    PADDED_MAIL = create_hp_armor('padded mail',          tier=6, defense=6,  hp=45)
    PLATE_ARMOR = create_def_armor('plate armor',         tier=8, defense=12, hp=40)
    LAMELLAR_ARMOR = create_hp_armor('lamellar armor',    tier=8, defense=8,  hp=60)

    # Runes
    ROCK = create_rune(libtcod.darker_gray, 'rock', None, throw_function=throw_std)
    RUNE_HEALING = create_rune(libtcod.green, 'rune of healing', heal, amount=0.5, weapon_amount=-2, armor_amount=5)
    RUNE_PAIN = create_rune(libtcod.red, 'rune of pain', pain, amount=0.5, weapon_amount=2, armor_amount=-5)
    RUNE_MIGHT = create_rune(libtcod.yellow, 'rune of might', might, amount=3, duration=10, weapon_amount=1)
    RUNE_PROTECTION = create_rune(libtcod.blue, 'rune of protection', protection, amount=3, duration=10, armor_amount=1)
    RUNE_TELEPORTATION = create_rune(libtcod.magenta, 'rune of teleportation', teleportation)
    RUNE_DIGGING = create_rune(libtcod.dark_sepia, 'rune of digging', digging)
    RUNE_REPLICATION = create_rune(libtcod.orange, 'rune of replication', replication)
    RUNE_CANCELLATION = create_rune(libtcod.darker_gray, 'rune of cancellation', cancellation)


def weight_range(value, start, end):
    weights = []
    for i in range(end + 2):
        if i in range(start, end):
            weights.append(value)
        else:
            weights.append(0)

    return weights


ENEMY_WEIGHTS = {
    EntityTemplates.GOBLIN:   [1, 2, 0],
    EntityTemplates.KOBOLD:   [2, 0],
    EntityTemplates.ZOMBIE:   [1, 2, 0],
    EntityTemplates.ORC:      [0, 1, 2, 1, 0],
    EntityTemplates.GNOLL:    [0, 0, 1, 3, 1, 1, 0],
    EntityTemplates.SKELETON: [0, 1, 2, 1, 0],
    EntityTemplates.SPIDER:   [0, 0, 0, 0, 1, 3, 3, 1, 0],
    EntityTemplates.WEREWOLF: [0, 0, 0, 2, 2, 2, 1, 0],
    EntityTemplates.OGRE:     [0, 0, 0, 0, 1, 3, 3, 1, 0],
    EntityTemplates.WYVERN:   [0, 0, 0, 0, 0, 0, 1, 2, 2, 1],
    EntityTemplates.CYCLOPS:  [0, 0, 0, 0, 0, 0, 1, 2, 2, 1],
    EntityTemplates.TROLL:    [0, 0, 0, 0, 0, 0, 1, 2, 2, 1],
    EntityTemplates.HYDRA:    [0, 0, 0, 0, 0, 0, 0, 0, 1, 2],
    EntityTemplates.MINOTAUR: [0, 0, 0, 0, 0, 0, 0, 0, 1, 2],
    EntityTemplates.DRAGON:   [0, 0, 0, 0, 0, 0, 0, 0, 1, 2]
}

ITEM_WEIGHTS = {
    EntityTemplates.DAGGER:        [2, 1, 0],
    EntityTemplates.SPEAR:         [2, 1, 0],
    EntityTemplates.CLUB:          [2, 1, 0],
    EntityTemplates.SHORTSWORD:    [0, 1, 2, 1, 0, 0],
    EntityTemplates.PIKE:          [0, 1, 2, 1, 0, 0],
    EntityTemplates.MACE:          [0, 1, 2, 1, 0, 0],
    EntityTemplates.ARMING_SWORD:  [0, 0, 0, 1, 2, 1, 0],
    EntityTemplates.POLEAXE:       [0, 0, 0, 1, 2, 1, 0],
    EntityTemplates.WARHAMMER:     [0, 0, 0, 1, 2, 1, 0],
    EntityTemplates.BASTARD_SWORD: [0, 0, 0, 0, 0, 1, 2, 1, 0],
    EntityTemplates.HALBERD:       [0, 0, 0, 0, 0, 1, 2, 1, 0],
    EntityTemplates.MORNING_STAR:  [0, 0, 0, 0, 0, 1, 2, 1, 0],
    EntityTemplates.LONGSWORD:     [0, 0, 0, 0, 0, 0, 0, 1, 2, 0],
    EntityTemplates.GLAIVE:        [0, 0, 0, 0, 0, 0, 0, 1, 2, 0],
    EntityTemplates.BATTLE_AXE:    [0, 0, 0, 0, 0, 0, 0, 1, 2, 0],

    EntityTemplates.LIGHT_HAUBERK:   [1, 2, 1, 0],
    EntityTemplates.GAMBESON:        [1, 2, 1, 0],
    EntityTemplates.FULL_HAUBERK:    [0, 0, 1, 2, 1, 0],
    EntityTemplates.LEATHER_CUIRASS: [0, 0, 1, 2, 1, 0],
    EntityTemplates.REINFORCED_MAIL: [0, 0, 0, 0, 1, 2, 1, 0],
    EntityTemplates.PADDED_MAIL:     [0, 0, 0, 0, 1, 2, 1, 0],
    EntityTemplates.PLATE_ARMOR:     [0, 0, 0, 0, 0, 0, 1, 2, 1, 0],
    EntityTemplates.LAMELLAR_ARMOR:  [0, 0, 0, 0, 0, 0, 1, 2, 1, 0],

    # The sum of rune weights should be about 18
    EntityTemplates.RUNE_HEALING: [6],
    EntityTemplates.RUNE_PAIN: [2],
    EntityTemplates.RUNE_MIGHT: [2],
    EntityTemplates.RUNE_PROTECTION: [2],
    EntityTemplates.RUNE_TELEPORTATION: [2],
    EntityTemplates.RUNE_DIGGING: [2],
    EntityTemplates.RUNE_REPLICATION: [2],
    EntityTemplates.RUNE_CANCELLATION: [2]
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
