import libtcodpy as libtcod


vk_key_map = {
    # Arrow keys
    libtcod.KEY_UP:     {'direction': (0, -1)},
    libtcod.KEY_DOWN:   {'direction': (0, 1)},
    libtcod.KEY_LEFT:   {'direction': (-1, 0)},
    libtcod.KEY_RIGHT:  {'direction': (1, 0)},
    # Number pad
    libtcod.KEY_KP1:    {'direction': (-1, 1)},
    libtcod.KEY_KP2:    {'direction': (0, 1)},
    libtcod.KEY_KP3:    {'direction': (1, 1)},
    libtcod.KEY_KP4:    {'direction': (-1, 0)},
    libtcod.KEY_KP6:    {'direction': (1, 0)},
    libtcod.KEY_KP7:    {'direction': (-1, -1)},
    libtcod.KEY_KP8:    {'direction': (0, -1)},
    libtcod.KEY_KP9:    {'direction': (1, -1)},

    libtcod.KEY_F11:    {'fullscreen': True},
    libtcod.KEY_ESCAPE: {'exit': True}
}


chr_key_map = {
    # WASD
    'w': {'direction': (0, -1)},
    's': {'direction': (0, 1)},
    'a': {'direction': (-1, 0)},
    'd': {'direction': (1, 0)},
    # VI keys
    'h': {'direction': (-1, 0)},
    'j': {'direction': (0, 1)},
    'k': {'direction': (0, -1)},
    'l': {'direction': (1, 0)},
    'y': {'direction': (-1, -1)},
    'u': {'direction': (1, -1)},
    'b': {'direction': (-1, 1)},
    'n': {'direction': (1, 1)}
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

    if vk_action is not None:
        return apply_modifiers(key, vk_action)

    if chr_action is not None:
        return apply_modifiers(key, chr_action)

    # No key was pressed
    return {}
