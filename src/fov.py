import libtcodpy as libtcod


def initialize_fov(game_map):
    fov_map = libtcod.map_new(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            libtcod.map_set_properties(fov_map, x, y, not game_map.get_tile(x, y).block_sight,
                                       not game_map.get_tile(x, y).blocked)

    return fov_map


def compute_fov(fov_map, memory, x, y, radius, light_walls=True, algorithm=0):
    libtcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)

    for xi in range(x - radius, x + radius):
        for yi in range(y - radius, y + radius):
            if libtcod.map_is_in_fov(fov_map, xi, yi):
                memory[xi][yi] = True
