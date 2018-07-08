import libtcodpy as libtcod


NORTH = {'direction': (0, -1)}
SOUTH = {'direction': (0, 1)}
WEST = {'direction': (-1, 0)}
EAST = {'direction': (1, 0)}
NORTHWEST = {'direction': (-1, -1)}
NORTHEAST = {'direction': (1, -1)}
SOUTHWEST = {'direction': (-1, 1)}
SOUTHEAST = {'direction': (1, 1)}

vk_key_map = {
    # Arrow keys
    libtcod.KEY_UP:     NORTH,
    libtcod.KEY_DOWN:   SOUTH,
    libtcod.KEY_LEFT:   WEST,
    libtcod.KEY_RIGHT:  EAST,
    # Number pad
    libtcod.KEY_KP1:    SOUTHWEST,
    libtcod.KEY_KP2:    SOUTH,
    libtcod.KEY_KP3:    SOUTHEAST,
    libtcod.KEY_KP4:    WEST,
    libtcod.KEY_KP6:    EAST,
    libtcod.KEY_KP7:    NORTHWEST,
    libtcod.KEY_KP8:    NORTH,
    libtcod.KEY_KP9:    NORTHEAST,

    libtcod.KEY_F11:    {'fullscreen': True},
    libtcod.KEY_ESCAPE: {'exit': True}
}

chr_key_map = {
    # WASD
    'w': NORTH,
    's': SOUTH,
    'a': WEST,
    'd': EAST,
    # VI keys
    'h': WEST,
    'j': SOUTH,
    'k': NORTH,
    'l': EAST,
    'y': NORTHWEST,
    'u': NORTHEAST,
    'b': SOUTHWEST,
    'n': SOUTHEAST
}


def apply_modifiers(key, action):
    if 'direction' in action.keys():
        if key.shift:
            action['face'] = True
            action['move'] = False
        elif key.lctrl:
            action['face'] = False
            action['move'] = True
        else:
            action['face'] = True
            action['move'] = True

    return action


def handle_keys(key):
    vk_action = vk_key_map.get(key.vk)
    chr_action = chr_key_map.get(chr(key.c))

    if vk_action:
        return apply_modifiers(key, vk_action)

    if chr_action:
        return apply_modifiers(key, chr_action)

    # No key was pressed
    return {}
