from enum import Enum

from map.dungeon_generator import *


class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """

    def __init__(self, blocks, blocks_sight=None, character=None):
        self.blocks = blocks

        # By default, if a tile is blocked, it also blocks sight
        self.blocks_sight = blocks_sight if blocks_sight else blocks

        if character is None:
            character = '#' if blocks else '.'

        self.character = character


class Tiles(Enum):
    ROOM_FLOOR = Tile(False)
    ROOM_WALL = Tile(True)
    CORRIDOR_FLOOR = Tile(False)
    CORRIDOR_WALL = Tile(True)
    CAVE_FLOOR = Tile(False)
    CAVE_WALL = Tile(True)
    DOOR = Tile(False, True, '+')


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
