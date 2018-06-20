import libtcodpy as libtcod


def render_all(console, game_map, entities, screen_width, screen_height):
    # Draw all the tiles in the game map
    for y in range(game_map.height):
        for x in range(game_map.width):
            libtcod.console_set_char_background(console, x, y, game_map.tiles[x][y].color, libtcod.BKGND_SET)

    # Draw all entities in the list
    for entity in entities:
        draw_entity(console, entity)

    libtcod.console_blit(console, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(console, entities):
    for entity in entities:
        clear_entity(console, entity)


def draw_entity(console, entity):
    libtcod.console_set_default_foreground(console, entity.color)
    libtcod.console_put_char(console, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(console, entity):
    # Erase the character that represents this object
    libtcod.console_put_char(console, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
