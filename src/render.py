from enum import Enum

import libtcodpy as libtcod
from libtcodpy import Color
from fov import distance


COLOR_UNKNOWN = libtcod.black


class RenderOrder(Enum):
    PLAYER = 0
    ENEMY = 1
    ITEM = 2
    CORPSE = 3


def render_all(console, entities, player, game_map, memory, fov_distance, screen_width, screen_height):
    # The center coordinates of the screen
    center_x = int(screen_width / 2)
    center_y = int(screen_height / 2)

    # Draw all visible and remembered tiles
    for x, y in memory:
        if libtcod.map_is_in_fov(game_map.fov_map, x, y):
            tile_color = apply_fov_gradient(game_map.get_tile(x, y).color, distance(player.x, player.y, x, y),
                                            fov_distance)
            libtcod.console_set_char_background(console, x - player.x + center_x, y - player.y + center_y, tile_color,
                                                libtcod.BKGND_SET)
        else:
            libtcod.console_set_char_background(console, x - player.x + center_x, y - player.y + center_y,
                                                game_map.get_tile(x, y).memory_color, libtcod.BKGND_SET)

    # Sort entities by their render order
    ordered_entities = sorted(entities, key=lambda i: i.render_order.value, reverse=True)

    # Draw all visible entities
    for entity in ordered_entities:
        if libtcod.map_is_in_fov(game_map.fov_map, entity.x, entity.y):
            libtcod.console_set_default_foreground(console, entity.color)
            libtcod.console_put_char(console, entity.x - player.x + int(screen_width / 2), entity.y - player.y +
                                     int(screen_height / 2), entity.char, libtcod.BKGND_NONE)

    libtcod.console_set_default_foreground(console, libtcod.white)
    libtcod.console_print_ex(console, 1, screen_height - 2, libtcod.BKGND_NONE, libtcod.LEFT,
                             'HP: {0:02}/{1:02}'.format(player.fighter.hp, player.fighter.max_hp))

    libtcod.console_blit(console, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(console, entities, player, screen_width, screen_height):
    for x in range(screen_width):
        for y in range(screen_height):
            libtcod.console_set_char_background(console, x, y, COLOR_UNKNOWN, libtcod.BKGND_SET)

    for entity in entities:
        libtcod.console_put_char(console, entity.x - player.x + int(screen_width / 2), entity.y - player.y +
                                 int(screen_height / 2), ' ', libtcod.BKGND_NONE)


# Used to brighten tiles near the player and darken ones further away
def apply_fov_gradient(tile_color, tile_distance, fov_distance, brightness_range=32, max_brightness=16):
    color_mod = int(brightness_range * (tile_distance / fov_distance)) - max_brightness

    # If the color modifier is above zero, the tile is darkened, otherwise it is lightened
    if color_mod >= 0:
        return tile_color.__sub__(Color(color_mod, color_mod, color_mod))
    else:
        color_mod = -color_mod
        return tile_color.__add__(Color(color_mod, color_mod, color_mod))
