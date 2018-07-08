import libtcodpy as libtcod
from libtcodpy import Color
from src.entity import distance
from src.map.game_map import COLOR_UNKNOWN


def render_all(console, entities, game_map, fov, memory, fov_distance, player_x, player_y, screen_width, screen_height):
    # The center coordinates of the screen
    center_x = int(screen_width / 2)
    center_y = int(screen_height / 2)

    # Draw all tiles in memory
    for (x, y) in memory:
        libtcod.console_set_char_background(console, x - player_x + center_x, y - player_y + center_y,
                                            game_map.get_tile(x, y).memory_color, libtcod.BKGND_SET)

    # Draw all currently visible tiles on top of remembered tiles
    for (x, y) in fov:
        tile_color = apply_fov_gradient(game_map.get_tile(x, y).color, distance(player_x, player_y, x, y), fov_distance)
        libtcod.console_set_char_background(console, x - player_x + center_x, y - player_y + center_y, tile_color,
                                            libtcod.BKGND_SET)

    # Draw all visible entities
    for entity in entities:
        if (entity.x, entity.y) in fov:
            libtcod.console_set_default_foreground(console, entity.color)
            libtcod.console_put_char(console, entity.x - player_x + int(screen_width / 2), entity.y - player_y +
                                     int(screen_height / 2), entity.char, libtcod.BKGND_NONE)

    libtcod.console_blit(console, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(console, entities, player_x, player_y, screen_width, screen_height):
    for x in range(screen_width):
        for y in range(screen_height):
            libtcod.console_set_char_background(console, x, y, COLOR_UNKNOWN, libtcod.BKGND_SET)

    for entity in entities:
        libtcod.console_put_char(console, entity.x - player_x + int(screen_width / 2), entity.y - player_y +
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
