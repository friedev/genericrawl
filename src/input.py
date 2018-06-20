import libtcodpy as libtcod

vk_key_map = {
    # Arrow keys
    libtcod.KEY_UP:     {'move': (0, -1)},
    libtcod.KEY_DOWN:   {'move': (0, 1)},
    libtcod.KEY_LEFT:   {'move': (-1, 0)},
    libtcod.KEY_RIGHT:  {'move': (1, 0)},
    # Number pad
    libtcod.KEY_KP1:    {'move': (-1, 1)},
    libtcod.KEY_KP2:    {'move': (0, 1)},
    libtcod.KEY_KP3:    {'move': (1, 1)},
    libtcod.KEY_KP4:    {'move': (-1, 0)},
    libtcod.KEY_KP6:    {'move': (1, 0)},
    libtcod.KEY_KP7:    {'move': (-1, -1)},
    libtcod.KEY_KP8:    {'move': (0, -1)},
    libtcod.KEY_KP9:    {'move': (1, -1)},

    libtcod.KEY_ESCAPE: {'exit': True}
}

chr_key_map = {
    # WASD
    'w': {'move': (0, -1)},
    's': {'move': (0, 1)},
    'a': {'move': (-1, 0)},
    'd': {'move': (1, 0)},
    # VI keys
    'h': {'move': (-1, 0)},
    'j': {'move': (0, 1)},
    'k': {'move': (0, -1)},
    'l': {'move': (1, 0)},
    'y': {'move': (-1, -1)},
    'u': {'move': (1, -1)},
    'b': {'move': (-1, 1)},
    'n': {'move': (1, 1)}
}


def handle_keys(key):
    # Toggle fullscreen (modifiers in control dict not yet supported)
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    vk_action = vk_key_map.get(key.vk)
    chr_action = chr_key_map.get(chr(key.c))

    if vk_action is not None:
        return vk_action

    if chr_action is not None:
        return chr_action

    # No key was pressed
    return {}
