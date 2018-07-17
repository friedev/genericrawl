from enum import Enum

import libtcodpy as libtcod


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


class InputScheme:
    def __init__(self, vk_key_map, chr_key_map):
        self.vk_key_map = vk_key_map
        self.chr_key_map = chr_key_map

    def handle_key(self, key):
        # Keys defined in this input scheme will take priority over the defaults
        action = self.vk_key_map.get(key.vk)

        if not action:
            action = self.chr_key_map.get(chr(key.c))

        # Fall back to the default key maps
        if not action and self is not GLOBAL:
            action = GLOBAL.handle_key(key)
            if action:
                return action
        elif action:
            return apply_modifiers(key, action)

        # No valid key was pressed
        return {}


NORTH = {'direction': (0, -1)}
SOUTH = {'direction': (0, 1)}
WEST = {'direction': (-1, 0)}
EAST = {'direction': (1, 0)}
NORTHWEST = {'direction': (-1, -1)}
NORTHEAST = {'direction': (1, -1)}
SOUTHWEST = {'direction': (-1, 1)}
SOUTHEAST = {'direction': (1, 1)}


GLOBAL = InputScheme({
    libtcod.KEY_UP:     NORTH,
    libtcod.KEY_DOWN:   SOUTH,
    libtcod.KEY_LEFT:   WEST,
    libtcod.KEY_RIGHT:  EAST,
    libtcod.KEY_F11:    {'fullscreen': True},
    libtcod.KEY_ESCAPE: {'exit': True}
}, {
    'g': {'pickup': True},
    ',': {'pickup': True},
    'i': {'inventory': True},
    ' ': {'wait': True},
    '.': {'wait': True},
    'r': {'restart': True}
})


class InputSchemes(Enum):
    LEFT_HAND = InputScheme({}, {
        'q': NORTHWEST,
        'w': NORTH,
        'e': NORTHEAST,
        'a': WEST,
        's': {'wait': True},
        'd': EAST,
        'z': SOUTHWEST,
        'x': SOUTH,
        'c': SOUTHEAST
    })

    VI = InputScheme({}, {
        'h': WEST,
        'j': SOUTH,
        'k': NORTH,
        'l': EAST,
        'y': NORTHWEST,
        'u': NORTHEAST,
        'b': SOUTHWEST,
        'n': SOUTHEAST
    })

    NUMPAD = InputScheme({
        libtcod.KEY_KP1:    SOUTHWEST,
        libtcod.KEY_KP2:    SOUTH,
        libtcod.KEY_KP3:    SOUTHEAST,
        libtcod.KEY_KP4:    WEST,
        libtcod.KEY_KP5:    {'wait': True},
        libtcod.KEY_KP6:    EAST,
        libtcod.KEY_KP7:    NORTHWEST,
        libtcod.KEY_KP8:    NORTH,
        libtcod.KEY_KP9:    NORTHEAST
    }, {})
