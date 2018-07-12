import libtcodpy as libtcod
from render import RenderOrder
from components.ai import BasicMonster
from components.fighter import Fighter
from components.sight import Sight
from entity import Entity
from map.dungeon_generator import *
from map.tile import Tiles, int_to_tile_map


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.generator = self.initialize_tiles()
        self.entities = []
        self.place_entities(int(width * height / 50))

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

    def place_entities(self, n_enemies):
        entity_map = self.generate_entity_map()

        for i in range(n_enemies):
            tile = self.find_open_tile()

            if randint(0, 3) < 3:
                sight_component = Sight()
                fighter_component = Fighter(hp=10, defense=1, power=3)
                ai_component = BasicMonster()
                entity = Entity(*tile, 'S', libtcod.yellow, 'python', render_order=RenderOrder.ENEMY,
                                sight=sight_component, fighter=fighter_component, ai=ai_component)
            else:
                sight_component = Sight()
                fighter_component = Fighter(hp=16, defense=1, power=4)
                ai_component = BasicMonster()
                entity = Entity(*tile, 'S', libtcod.blue, 'blue python', render_order=RenderOrder.ENEMY,
                                sight=sight_component,
                                fighter=fighter_component, ai=ai_component)
                # TODO be more creative

            self.entities.append(entity)
            entity_map[entity.x][entity.y].append(entity)

    def generate_fov_map(self):
        fov_map = libtcod.map_new(self.width, self.height)

        for x in range(self.width):
            for y in range(self.height):
                libtcod.map_set_properties(fov_map, x, y, not self.get_tile(x, y).blocks_sight,
                                           not self.get_tile(x, y).blocks)

        return fov_map

    def generate_fov_map_with_entities(self, exclude=[]):
        fov_map = self.generate_fov_map()

        for entity in self.entities:
            if entity.blocks and entity not in exclude:
                libtcod.map_set_properties(fov_map, entity.x, entity.y, True, False)

        return fov_map

    def get_tile(self, x, y):
        return int_to_tile_map.get(self.generator.grid[x][y]).value

    def is_tile_open(self, x, y, entity_map=None):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        if self.get_tile(x, y).blocks:
            return False

        blocking_entities = self.get_entities_at_tile(x, y, True, entity_map)
        return len(blocking_entities) == 0

    def get_entities_at_tile(self, x, y, blocking_only=False, entity_map=None):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        if not entity_map:
            tile_entities = []
            for entity in self.entities:
                if entity.x == x and entity.y == y:
                    if blocking_only and not entity.blocks:
                        continue
                    tile_entities.append(entity)
            return tile_entities
        elif blocking_only:
            tile_entities = []
            for entity in entity_map[x][y]:
                if entity.blocks:
                    tile_entities.append(entity)
            return tile_entities
        else:
            return entity_map[x][y]

    def find_open_tile(self, entity_map=None):
        if not entity_map:
            entity_map = self.generate_entity_map()

        open_tiles = []

        for x in range(self.generator.width):
            for y in range(self.generator.height):
                if self.is_tile_open(x, y, entity_map):
                    open_tiles.append((x, y))

        return choice(open_tiles)

    # Returns a 3D list, where the first two dimensions are the same as the game map
    # The third dimension is a list of the entities in that tile
    def generate_entity_map(self):
        entity_map = [[[] for y in range(self.height)] for x in range(self.width)]
        for entity in self.entities:
            entity_map[entity.x][entity.y].append(entity)
        return entity_map
