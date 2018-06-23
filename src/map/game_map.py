import libtcodpy as libtcod
from src.map.dungeon_generator import *
from src.map.tile import Tile

TILE_ROOM_FLOOR = Tile(libtcod.light_blue, False)
TILE_ROOM_WALL = Tile(libtcod.dark_blue, True)
TILE_CORRIDOR_FLOOR = Tile(libtcod.gray, False)
TILE_CORRIDOR_WALL = Tile(libtcod.darker_gray, True)
TILE_DOOR = Tile(libtcod.dark_cyan, False, True)
TILE_CAVE_FLOOR = Tile(libtcod.darker_orange, False)
TILE_CAVE_WALL = Tile(libtcod.darkest_orange, True)
COLOR_UNKNOWN = libtcod.black

int_to_tile = {
    EMPTY:         TILE_CAVE_WALL,
    FLOOR:         TILE_ROOM_FLOOR,
    CORRIDOR:      TILE_CORRIDOR_FLOOR,
    DOOR:          TILE_DOOR,
    DEADEND:       TILE_CORRIDOR_FLOOR,
    ROOM_WALL:     TILE_ROOM_WALL,
    CORRIDOR_WALL: TILE_CORRIDOR_WALL,
    CAVE_WALL:     TILE_CAVE_WALL,
    CAVE:          TILE_CAVE_FLOOR
}


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.generator = self.initialize_tiles()

    def initialize_tiles(self):
        # Dungeon size adjusted by 2 to ensure perimeter walls
        generator = dungeonGenerator(self.height - 2, self.width - 2)
        generator.generateCaves(37, 4)

        # Remove small caves
        unconnected = generator.findUnconnectedAreas()
        for area in unconnected:
            if len(area) < 35:
                for x, y in area:
                    generator.grid[x][y] = EMPTY

        # Generate rooms and corridors
        generator.placeRandomRooms(5, 9, 1, 1, 2000)
        x, y = generator.findEmptySpace(3)
        while x:
            generator.generateCorridors('l', x, y)
            x, y = generator.findEmptySpace(3)

        # Join rooms, caves, and corridors
        generator.connectAllRooms(0)
        unconnected = generator.findUnconnectedAreas()
        generator.joinUnconnectedAreas(unconnected)
        generator.pruneDeadends(70)
        generator.placeWalls()

        # Create a copy of the grid, acting as a buffer for the next step
        grid_copy = [[CAVE_WALL for y in range(self.height)] for x in range(self.width)]

        for x in range(generator.width):
            for y in range(generator.height):
                grid_copy[x + 1][y + 1] = generator.grid[x][y]

        # Expand all room floors by 1 tile to fill doorways
        for x in range(generator.width):
            for y in range(generator.height):
                if generator.grid[x][y] == FLOOR:
                    for nx, ny in generator.findNeighboursDirect(x, y):
                        if generator.grid[nx][ny] == CORRIDOR or generator.grid[nx][ny] == CAVE:
                            grid_copy[nx + 1][ny + 1] = FLOOR

        generator.grid = grid_copy

        return generator

    def get_tile(self, x, y):
        return int_to_tile.get(self.generator.grid[x][y])
