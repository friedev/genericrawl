from math import atan2, cos, pi, sin, sqrt

import tcod


def distance(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    return sqrt(dx ** 2 + dy ** 2)


def compute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0, memory=None):
    tcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)

    if memory is not None:
        # Must use "is not None" because [] also evaluates to False
        for xi in range(x - radius, x + radius):
            for yi in range(y - radius, y + radius):
                if tcod.map_is_in_fov(fov_map, xi, yi):
                    memory[xi][yi] = True


def compute_fov_angled(fov_map, x, y, radius, angle, span, light_walls=True, algorithm=0, memory=None,
                       reveal_sides=True):
    compute_fov(fov_map, x, y, radius, light_walls, algorithm)

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

    for xi in range(x - radius, x + radius):
        for yi in range(y - radius, y + radius):
            if tcod.map_is_in_fov(fov_map, xi, yi):
                x_rel = xi - x
                y_rel = yi - y
                tile_angle = atan2(y_rel, x_rel)

                if swap_angles == (lesser_angle <= tile_angle <= greater_angle):
                    tcod.map_set_in_fov(fov_map, xi, yi, False)
                elif memory is not None:
                    # Must use "is not None" because [] also evaluates to False
                    memory[xi][yi] = True

    tcod.map_set_in_fov(fov_map, x, y, True)
    memory[x][y] = True

    if reveal_sides:
        # Ideal, angle-based approach (some issues with signs result in incorrect
        # left_angle = angle - (pi / 2)
        # right_angle = angle + (pi / 2)
        #
        # left_x = int(x + cos(left_angle))
        # left_y = int(y + sin(left_angle))
        # right_x = int(x + cos(right_angle))
        # right_y = int(y + sin(right_angle))

        facing_x = int(round(cos(angle)))
        facing_y = int(round(sin(angle)))

        if facing_x == 0:
            left_x = -1
            left_y = 0
            right_x = 1
            right_y = 0
        elif facing_y == 0:
            left_x = 0
            left_y = -1
            right_x = 0
            right_y = 1
        else:
            left_x = facing_x
            left_y = -facing_y
            right_x = -facing_x
            right_y = facing_y

        tcod.map_set_in_fov(fov_map, x + left_x, y + left_y, True)
        tcod.map_set_in_fov(fov_map, x + right_x, y + right_y, True)

        memory[x + left_x][y + left_y] = True
        memory[x + right_x][y + right_y] = True
