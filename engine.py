import libtcodpy as libtcod
from src.entity import Entity
from src.input import handle_keys
from src.map.game_map import GameMap
from src.map.tile import Tile
from src.render import render_all, clear_all


def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45
    floor = Tile(libtcod.gray, False)
    wall = Tile(libtcod.dark_orange, True)

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)
    entities = [npc, player]

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'GeneriCrawl', False)

    console = libtcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height, floor, wall)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        render_all(console, game_map, entities, screen_width, screen_height)
        libtcod.console_flush()
        libtcod.sys_wait_for_event(libtcod.EVENT_KEY_PRESS, key, mouse, True)
        clear_all(console, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player.move(dx, dy, game_map)

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
