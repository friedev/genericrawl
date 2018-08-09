from src.components.item import *
from src.entity_templates import ENEMY_WEIGHTS, weighted_choice, get_weights_for_level, ITEM_WEIGHTS
from src.map.dungeon_generator import *
from src.map.tile import int_to_tile_map, Tiles


def generate_dungeon(**kwargs):
    width = kwargs.get('width')
    height = kwargs.get('height')

    # Dungeon size adjusted by 2 to ensure perimeter walls
    generator = dungeonGenerator(height - 2, width - 2)

    caves = kwargs.get('caves')
    if caves:
        generator.generateCaves(caves)

        min_cave_size = kwargs.get('min_cave_size')
        if min_cave_size:
            # Remove small caves
            unconnected = generator.findUnconnectedAreas()
            for area in unconnected:
                if len(area) < min_cave_size:
                    for x, y in area:
                        generator.grid[x][y] = EMPTY

    # Generate rooms and corridors
    generator.placeRandomRooms(kwargs.get('min_room_size'), kwargs.get('max_room_size'),
                               attempts=kwargs.get('max_rooms'))
    x, y = generator.findEmptySpace(3)
    while x:
        generator.generateCorridors('l', x, y)
        x, y = generator.findEmptySpace(3)

    # Join rooms, caves, and corridors
    generator.connectAllRooms(kwargs.get('extra_door_chance'))
    unconnected = generator.findUnconnectedAreas()
    generator.joinUnconnectedAreas(unconnected)
    generator.pruneDeadends(kwargs.get('prune_deadends'))
    generator.placeWalls()

    # Create a copy of the grid, acting as a buffer for the next step
    grid_copy = [[CAVE_WALL for y in range(height)] for x in range(width)]

    for x in range(generator.width):
        for y in range(generator.height):
            grid_copy[x + 1][y + 1] = generator.grid[x][y]

    # Expand all room floors by 1 tile to fill doorways, recording room floors at the same time
    floors = []
    for x in range(generator.width):
        for y in range(generator.height):
            if generator.grid[x][y] == ROOM_FLOOR:
                if not kwargs.get('cave_stairs'):
                    floors.append((x, y))
                for nx, ny in generator.findNeighboursDirect(x, y):
                    if generator.grid[nx][ny] == CORRIDOR_FLOOR or generator.grid[nx][ny] == CAVE_FLOOR:
                        grid_copy[nx + 1][ny + 1] = ROOM_FLOOR

    if kwargs.get('cave_stairs'):
        for x in range(generator.width):
            for y in range(generator.height):
                if generator.grid[x][y] is CAVE_FLOOR:
                    floors.append((x, y))

    for i in range(kwargs.get('stairs')):
        stair_x, stair_y = choice(floors)
        floors.remove((stair_x, stair_y))
        grid_copy[stair_x + 1][stair_y + 1] = STAIRS

    generator.grid = grid_copy
    generator.width = width
    generator.height = height
    return generator


def generate_caves(**kwargs):
    width = kwargs.get('width')
    height = kwargs.get('height')

    # Dungeon size adjusted by 2 to ensure perimeter walls
    generator = dungeonGenerator(height - 2, width - 2)

    caves = kwargs.get('caves')
    if caves:
        generator.generateCaves(caves)

        min_cave_size = kwargs.get('min_cave_size')
        if min_cave_size:
            # Remove small caves
            unconnected = generator.findUnconnectedAreas()
            for area in unconnected:
                if len(area) < min_cave_size:
                    for x, y in area:
                        generator.grid[x][y] = EMPTY

    unconnected = generator.findUnconnectedAreas()
    generator.joinUnconnectedAreas(unconnected)
    generator.placeWalls()

    # Create a copy of the grid, acting as a buffer for the next step
    grid_copy = [[CAVE_WALL for y in range(height)] for x in range(width)]

    for x in range(generator.width):
        for y in range(generator.height):
            grid_copy[x + 1][y + 1] = generator.grid[x][y]

    floors = []
    for x in range(generator.width):
        for y in range(generator.height):
            if generator.grid[x][y] is CAVE_FLOOR or generator.grid[x][y] is CORRIDOR_FLOOR:
                floors.append((x, y))

    for i in range(kwargs.get('stairs')):
        stair_x, stair_y = choice(floors)
        floors.remove((stair_x, stair_y))
        grid_copy[stair_x + 1][stair_y + 1] = STAIRS

    generator.width = width
    generator.height = height
    generator.grid = grid_copy
    return generator


LEVEL_CONFIGURATIONS = {
    1: {'tiles_per_enemy': 50, 'tiles_per_item': 40, 'start_tile': Tiles.ROOM_FLOOR, 'generator': generate_dungeon,
        'generator_kwargs': {'width': 40, 'height': 40, 'min_room_size': 4, 'max_room_size': 7,

                             'max_rooms': 100, 'extra_door_chance': 20,  'prune_deadends': 10, 'stairs': 2}},
    2: {'tiles_per_enemy': 40, 'tiles_per_item': 45, 'start_tile': Tiles.ROOM_FLOOR, 'generator': generate_dungeon,
        'generator_kwargs': {'width': 55, 'height': 55, 'min_room_size': 4, 'max_room_size': 8,
                             'max_rooms': 150, 'extra_door_chance': 20,  'prune_deadends': 10, 'stairs': 2}},

    3: {'tiles_per_enemy': 30, 'tiles_per_item': 50, 'start_tile': Tiles.ROOM_FLOOR, 'generator': generate_dungeon,
        'generator_kwargs': {'width': 70, 'height': 70, 'min_room_size': 5, 'max_room_size': 9,
                             'max_rooms': 200, 'extra_door_chance': 20,  'prune_deadends': 5, 'stairs': 3}},

    4: {'tiles_per_enemy': 35, 'tiles_per_item': 55, 'start_tile': Tiles.ROOM_FLOOR, 'generator': generate_dungeon,
        'generator_kwargs': {'width': 60, 'height': 60, 'min_room_size': 4, 'max_room_size': 8,
                             'max_rooms': 200, 'extra_door_chance': 20, 'prune_deadends': 10, 'stairs': 3,
                             'caves': 37, 'min_cave_size': 25}},

    5: {'tiles_per_enemy': 40, 'tiles_per_item': 55, 'start_tile': Tiles.ROOM_FLOOR,
        'tile_overrides': {STAIRS: Tiles.CAVE_STAIRS}, 'generator': generate_dungeon,
        'generator_kwargs': {'width': 50, 'height': 50, 'min_room_size': 4, 'max_room_size': 7,
                             'max_rooms': 200, 'extra_door_chance': 20, 'prune_deadends': 10, 'stairs': 2,
                             'caves': 40, 'min_cave_size': 25, 'cave_stairs': True}},

    6: {'tiles_per_enemy': 60, 'tiles_per_item': 60, 'start_tile': Tiles.CAVE_FLOOR,
        'tile_overrides': {CORRIDOR_FLOOR: Tiles.CAVE_FLOOR, CORRIDOR_WALL: Tiles.CAVE_WALL,
                           STAIRS: Tiles.CAVE_STAIRS}, 'generator': generate_caves,
        'generator_kwargs': {'width': 60, 'height': 60, 'caves': 40, 'min_cave_size': 35, 'stairs': 3}},

    7: {'tiles_per_enemy': 50, 'tiles_per_item': 55, 'start_tile': Tiles.CAVE_FLOOR,
        'tile_overrides': {CORRIDOR_FLOOR: Tiles.CAVE_FLOOR, CORRIDOR_WALL: Tiles.CAVE_WALL,
                           STAIRS: Tiles.CAVE_STAIRS}, 'generator': generate_caves,
        'generator_kwargs': {'width': 75, 'height': 75, 'caves': 40, 'min_cave_size': 35, 'stairs': 3}},

    8: {'tiles_per_enemy': 40, 'tiles_per_item': 50, 'start_tile': Tiles.CAVE_FLOOR,
        'tile_overrides': {CORRIDOR_FLOOR: Tiles.CAVE_FLOOR, CORRIDOR_WALL: Tiles.CAVE_WALL,
                           STAIRS: Tiles.CAVE_STAIRS}, 'generator': generate_caves,
        'generator_kwargs': {'width': 90, 'height': 90, 'caves': 40, 'min_cave_size': 35, 'stairs': 4}},

    9: {'tiles_per_enemy': 30, 'tiles_per_item': 40, 'start_tile': Tiles.CAVE_FLOOR, 'generator': generate_dungeon,
        'generator_kwargs': {'width': 70, 'height': 60, 'min_room_size': 5, 'max_room_size': 10,
                             'max_rooms': 200, 'extra_door_chance': 30, 'prune_deadends': 1, 'stairs': 3,
                             'caves': 37, 'min_cave_size': 25}},

    10: {'tiles_per_enemy': 20, 'tiles_per_item': 30, 'start_tile': Tiles.CORRIDOR_FLOOR, 'generator': generate_dungeon,
         'generator_kwargs': {'width': 80, 'height': 80, 'min_room_size': 8, 'max_room_size': 14,
                              'max_rooms': 1, 'extra_door_chance': 30,  'prune_deadends': 1, 'stairs': 1}},
}


class GameMap:
    def __init__(self, dungeon_level):
        configuration = LEVEL_CONFIGURATIONS.get(dungeon_level)
        self.dungeon_level = dungeon_level
        self.generator = configuration['generator'](**configuration.get('generator_kwargs'))

        self.tile_overrides = configuration.get('tile_overrides')
        if not self.tile_overrides:
            self.tile_overrides = {}

        self.entities = []
        self.place_entities(configuration.get('tiles_per_enemy'), configuration.get('tiles_per_item'))

    @property
    def width(self):
        return self.generator.width

    @property
    def height(self):
        return self.generator.height

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

        # Expand all room floors by 1 tile to fill doorways, recording room floors at the same time
        room_floors = []
        for x in range(generator.width):
            for y in range(generator.height):
                if generator.grid[x][y] == ROOM_FLOOR:
                    room_floors.append((x, y))
                    for nx, ny in generator.findNeighboursDirect(x, y):
                        if generator.grid[nx][ny] == CORRIDOR_FLOOR or generator.grid[nx][ny] == CAVE_FLOOR:
                            grid_copy[nx + 1][ny + 1] = ROOM_FLOOR

        stair_x, stair_y = choice(room_floors)
        grid_copy[stair_x + 1][stair_y + 1] = STAIRS

        generator.grid = grid_copy
        return generator

    def place_entities(self, tiles_per_enemy, tiles_per_item):
        level_enemy_weights = get_weights_for_level(ENEMY_WEIGHTS, self.dungeon_level)
        level_item_weights = get_weights_for_level(ITEM_WEIGHTS, self.dungeon_level)

        open_tiles = self.get_all_open_tiles(include_entities=False)

        # Unoccupied tiles refers to open tiles with no enemies in them
        unoccupied_tiles = open_tiles.copy()
        n_enemies = int(len(open_tiles) / tiles_per_enemy)
        for i in range(n_enemies):
            # The tile in which this entity is placed will no longer be unoccupied
            tile = choice(unoccupied_tiles)
            unoccupied_tiles.remove(tile)

            enemy = weighted_choice(level_enemy_weights).value.clone(*tile)
            self.entities.append(enemy)

        n_items = int(len(open_tiles) / tiles_per_item)
        for i in range(n_items):
            # The tile in which this item is placed will no longer be open
            tile = choice(open_tiles)
            open_tiles.remove(tile)

            item = weighted_choice(level_item_weights).value.clone(*tile)
            self.entities.append(item)

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

    def contains(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_tile(self, x, y, raw=False, value=True):
        int_tile = self.generator.grid[x][y]

        if raw:
            return int_tile

        obj_tile = self.tile_overrides.get(int_tile)
        if not obj_tile:
            obj_tile = int_to_tile_map.get(int_tile)

        return obj_tile.value if value else obj_tile

    def is_tile_open(self, x, y, check_entities=True, entity_map=None):
        if not self.contains(x, y) or self.get_tile(x, y).blocks:
            return False

        if not check_entities:
            return True

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

    def find_open_tile(self, tile_type=None, include_entities=True, entity_map=None):
        return choice(self.get_all_open_tiles(tile_type, include_entities, entity_map))

    def get_all_open_tiles(self, tile_type=None, include_entities=True, entity_map=None):
        if not entity_map:
            entity_map = self.generate_entity_map()

        open_tiles = []

        for x in range(self.generator.width):
            for y in range(self.generator.height):
                if self.is_tile_open(x, y, include_entities, entity_map):
                    if not tile_type or tile_type is self.get_tile(x, y, value=False):
                        open_tiles.append((x, y))

        return open_tiles

    # Returns a 3D list, where the first two dimensions are the same as the game map
    # The third dimension is a list of the entities in that tile
    def generate_entity_map(self):
        entity_map = [[[] for y in range(self.height)] for x in range(self.width)]
        for entity in self.entities:
            entity_map[entity.x][entity.y].append(entity)
        return entity_map
