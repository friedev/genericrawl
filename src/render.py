import libtcodpy as libtcod
from src.map.game_map import COLOR_UNKNOWN


def render_all(console, entities, game_map, fov, memory, screen_width, screen_height):
    # Draw all the tiles in the game map
    for y in range(game_map.height):
        for x in range(game_map.width):
            visible = (x, y) in fov
            remembered = (x, y) in memory

            if visible:
                color = game_map.get_tile(x, y).color
            elif remembered:
                color = game_map.get_tile(x, y).memory_color
            else:
                color = COLOR_UNKNOWN

            libtcod.console_set_char_background(console, x, y, color, libtcod.BKGND_SET)

    # Draw all entities in the list
    for entity in entities:
        draw_entity(console, entity, fov)

    libtcod.console_blit(console, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(console, entities):
    for entity in entities:
        clear_entity(console, entity)


def draw_entity(console, entity, fov):
    if (entity.x, entity.y) in fov:
        libtcod.console_set_default_foreground(console, entity.color)
        libtcod.console_put_char(console, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(console, entity):
    # Erase the character that represents this object
    libtcod.console_put_char(console, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
