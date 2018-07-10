from enum import Enum

import libtcodpy as libtcod
from libtcodpy import Color
from map.dungeon_generator import *


class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """

    def __init__(self, color, blocks, blocks_sight=None, memory_color=None):
        self.color = color
        self.blocks = blocks

        # By default, if a tile is blocked, it also blocks sight
        if not blocks_sight:
            blocks_sight = blocks

        self.blocks_sight = blocks_sight

        if not memory_color:
            memory_color = color.__sub__(Color(32, 32, 32))

        self.memory_color = memory_color


class Tiles(Enum):
    ROOM_FLOOR = Tile(libtcod.light_blue, False)
    ROOM_WALL = Tile(libtcod.dark_blue, True)
    CORRIDOR_FLOOR = Tile(libtcod.gray, False)
    CORRIDOR_WALL = Tile(libtcod.darker_gray, True)
    DOOR = Tile(libtcod.dark_cyan, False, True)
    CAVE_FLOOR = Tile(libtcod.darker_orange, False)
    CAVE_WALL = Tile(libtcod.darkest_orange, True)


int_to_tile_map = {
    EMPTY:         Tiles.CAVE_WALL,
    FLOOR:         Tiles.ROOM_FLOOR,
    CORRIDOR:      Tiles.CORRIDOR_FLOOR,
    DOOR:          Tiles.DOOR,
    DEADEND:       Tiles.CORRIDOR_FLOOR,
    ROOM_WALL:     Tiles.ROOM_WALL,
    CORRIDOR_WALL: Tiles.CORRIDOR_WALL,
    CAVE_WALL:     Tiles.CAVE_WALL,
    CAVE:          Tiles.CAVE_FLOOR
}
