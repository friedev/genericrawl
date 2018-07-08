import libtcodpy as libtcod
from math import atan2, pi


def initialize_fov(game_map):
    fov_map = libtcod.map_new(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            libtcod.map_set_properties(fov_map, x, y, not game_map.get_tile(x, y).blocks_sight,
                                       not game_map.get_tile(x, y).blocks)

    return fov_map


def compute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    libtcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)

    fov = []

    for xi in range(x - radius, x + radius):
        for yi in range(y - radius, y + radius):
            if libtcod.map_is_in_fov(fov_map, xi, yi):
                fov.append((xi, yi))

    return fov


def compute_fov_angled(fov_map, x, y, radius, angle, span, light_walls=True, algorithm=0):
    fov_full = compute_fov(fov_map, x, y, radius, light_walls, algorithm)
    fov_angled = []

    angle1 = angle - span / 2.0
    angle2 = angle + span / 2.0

    swap_angles = False
    if angle1 < -pi:
        angle1 += 2 * pi
        swap_angles = True

    if angle2 > pi:
        angle2 -= 2 * pi
        swap_angles = True

    greater_angle = max(angle1, angle2)
    lesser_angle = min(angle1, angle2)

    for xi, yi in fov_full:
        x_rel = xi - x
        y_rel = yi - y
        tile_angle = atan2(y_rel, x_rel)

        if swap_angles != (lesser_angle <= tile_angle <= greater_angle):
            fov_angled.append((xi, yi))

    if not (x, y) in fov_angled:
        fov_angled.append((x, y))

    return fov_angled


def update_memory(memory, fov):
    for (x, y) in fov:
        if (x, y) not in memory:
            memory.append((x, y))

    return memory
