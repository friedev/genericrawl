import libtcodpy as libtcod


def render_all(console, entities, screen_width, screen_height):
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
