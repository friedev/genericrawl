from enum import Enum

import libtcodpy as libtcod
from fov import distance
from game_messages import Message
from libtcodpy import Color

COLOR_UNKNOWN = libtcod.black


class RenderOrder(Enum):
    PLAYER = 0
    ENEMY = 1
    ITEM = 2
    CORPSE = 3


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))


def render_all(console, panel, bar_width, message_log, game_map, player, fov_map, memory, mouse):
    # Screen dimensions
    screen_width = libtcod.console_get_width(console)
    screen_height = libtcod.console_get_height(console)

    # The center coordinates of the screen
    center_x = int(screen_width / 2)
    center_y = int(screen_height / 2)

    # The map coordinates of the top left character displayed on the screen
    top_left_x = player.x - center_x
    top_left_y = player.y - center_y

    # Draw all visible and remembered tiles
    for x, y in memory:
        if libtcod.map_is_in_fov(fov_map, x, y):
            tile_color = apply_fov_gradient(game_map.get_tile(x, y).color, distance(player.x, player.y, x, y),
                                            player.sight.fov_radius)
            libtcod.console_set_char_background(console, x - top_left_x, y - top_left_y, tile_color,
                                                libtcod.BKGND_SET)
        else:
            libtcod.console_set_char_background(console, x - top_left_x, y - top_left_y,
                                                game_map.get_tile(x, y).memory_color, libtcod.BKGND_SET)

    # Sort entities by their render order
    ordered_entities = sorted(game_map.entities, key=lambda i: i.render_order.value, reverse=True)

    # Draw all visible entities
    for entity in ordered_entities:
        if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            libtcod.console_set_default_foreground(console, entity.color)
            libtcod.console_put_char(console, entity.x - top_left_x, entity.y - top_left_y, entity.char,
                                     libtcod.BKGND_NONE)

    libtcod.console_blit(console, 0, 0, screen_width, screen_height, 0, 0, 0)

    # Panel dimensions
    panel_width = libtcod.console_get_width(panel)
    panel_height = libtcod.console_get_height(panel)
    panel_y = screen_height - panel_height

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    cursor_x = mouse.cx + top_left_x
    cursor_y = mouse.cy + top_left_y
    if mouse.lbutton_pressed and libtcod.map_is_in_fov(fov_map, cursor_x, cursor_y):
        entities_at_cursor = game_map.get_entities_at_tile(cursor_x, cursor_y)
        if entities_at_cursor:
            names = [entity.indefinite_name() for entity in entities_at_cursor]
            name_len = len(names)
            names = 'You see ' + ', '.join(names) + '.'
            names = names.rsplit(',', 1)
            if name_len > 2:
                names = ', and'.join(names)
            else:
                names = ' and'.join(names)
            message_log.add_message(Message(names, libtcod.light_gray))

    # Print the game messages, one line at a time
    message_y = 0
    for i in range(max(0, len(message_log.messages) - panel_height), max(0, len(message_log.messages))):
        message = message_log.messages[i]
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, message_y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        message_y += 1

    render_bar(panel, 1, 0, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)

    libtcod.console_blit(panel, 0, 0, panel_width, panel_height, 0, 0, panel_y)


def clear_all(console, entities, player, screen_width, screen_height):
    for x in range(screen_width):
        for y in range(screen_height):
            libtcod.console_set_char_background(console, x, y, COLOR_UNKNOWN, libtcod.BKGND_SET)

    for entity in entities:
        libtcod.console_put_char(console, entity.x - player.x + int(screen_width / 2), entity.y - player.y +
                                 int(screen_height / 2), ' ', libtcod.BKGND_NONE)


# Used to brighten tiles near the player and darken ones further away
def apply_fov_gradient(tile_color, tile_distance, fov_radius, brightness_range=32, max_brightness=16):
    color_mod = int(brightness_range * (tile_distance / fov_radius)) - max_brightness

    # If the color modifier is above zero, the tile is darkened, otherwise it is lightened
    if color_mod >= 0:
        return tile_color.__sub__(Color(color_mod, color_mod, color_mod))
    else:
        color_mod = -color_mod
        return tile_color.__add__(Color(color_mod, color_mod, color_mod))
