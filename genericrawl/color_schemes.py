from enum import Enum

import tcod
from tcod import Color

from .map.tile import Tiles


def generate_tile_dict(room_floor, room_wall, corridor_floor, corridor_wall, cave_floor, cave_wall, door, room_stairs,
                       cave_stairs, unknown=tcod.black):
    return {
        Tiles.ROOM_FLOOR:     room_floor,
        Tiles.ROOM_WALL:      room_wall,
        Tiles.CORRIDOR_FLOOR: corridor_floor,
        Tiles.CORRIDOR_WALL:  corridor_wall,
        Tiles.CAVE_FLOOR:     cave_floor,
        Tiles.CAVE_WALL:      cave_wall,
        Tiles.DOOR:           door,
        Tiles.ROOM_STAIRS:    room_stairs,
        Tiles.CAVE_STAIRS:    cave_stairs,
        None:                 unknown
    }


def generate_monochrome_dict(color):
    return generate_tile_dict(color, color, color, color, color, color, color, color, color)


def color_dict_change_brightness(color_dict, mod):
    copy = color_dict.copy()
    for key in copy.keys():
        if mod > 0:
            copy[key] = copy[key].__add__(Color(mod, mod, mod))
        else:
            copy[key] = copy[key].__sub__(Color(-mod, -mod, -mod))
    return copy


# A convenience method that allows color dicts to be modified when initialized in the ColorSchemes enum
def set_tile_color(color_dict, tile, color):
    copy = color_dict.copy()
    copy[tile] = color
    return copy


DEFAULT_COLORS = generate_tile_dict(tcod.light_blue, tcod.dark_blue, tcod.gray, tcod.darker_gray,
                                    tcod.dark_sepia, tcod.darker_sepia, tcod.dark_cyan,
                                    tcod.light_blue, tcod.dark_sepia)


class ColorScheme:
    def __init__(self, name, foreground=DEFAULT_COLORS, background=DEFAULT_COLORS, memory_brightness_mod=32,
                 allow_fade=True):
        self.name = name
        self.background = background if background else generate_monochrome_dict(tcod.black)
        self.foreground = foreground if foreground else background
        self.memory_brightness_mod = memory_brightness_mod
        self.allow_fade = allow_fade

    def get_memory_color(self, color):
        return color.__sub__(Color(self.memory_brightness_mod, self.memory_brightness_mod, self.memory_brightness_mod))


class ColorSchemes(Enum):
    CLASSIC = ColorScheme('Classic', foreground=generate_monochrome_dict(tcod.lightest_gray), background=None,
                          memory_brightness_mod=64, allow_fade=False)
    CLASSIC_COLORED = ColorScheme('Classic Colored', foreground=color_dict_change_brightness(DEFAULT_COLORS, 32),
                                  background=None, allow_fade=False)
    SOLID_WALLS = ColorScheme('Solid Walls', background=None)
    SOLID = ColorScheme('Solid')
    COMBO = ColorScheme('Combo', foreground=color_dict_change_brightness(DEFAULT_COLORS, 32))


def init_color_schemes():
    ColorSchemes.CLASSIC.value.foreground = set_tile_color(ColorSchemes.CLASSIC.value.foreground, Tiles.DOOR,
                                                           tcod.dark_yellow)

    solid_walls_background = ColorSchemes.SOLID_WALLS.value.background
    solid_walls_background = set_tile_color(solid_walls_background, Tiles.ROOM_WALL,
                                            DEFAULT_COLORS.get(Tiles.ROOM_WALL))
    solid_walls_background = set_tile_color(solid_walls_background, Tiles.CORRIDOR_WALL,
                                            DEFAULT_COLORS.get(Tiles.CORRIDOR_WALL))
    solid_walls_background = set_tile_color(solid_walls_background, Tiles.CAVE_WALL, DEFAULT_COLORS.get(
        Tiles.CAVE_WALL))
    ColorSchemes.SOLID_WALLS.value.background = solid_walls_background

    for scheme in ColorSchemes:
        scheme.value.foreground = set_tile_color(scheme.value.foreground, Tiles.ROOM_STAIRS, tcod.white)
        scheme.value.foreground = set_tile_color(scheme.value.foreground, Tiles.CAVE_STAIRS, tcod.white)
