import libtcodpy as libtcod
from src.entity import Entity
from src.fov import initialize_fov, compute_fov
from src.input import handle_keys
from src.map.game_map import GameMap
from src.render import render_all, clear_all


def main():
    screen_width = 80
    screen_height = 50

    map_width = screen_width
    map_height = screen_height

    fov_radius = 10

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)
    entities = [npc, player]

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'GeneriCrawl', False)

    console = libtcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)

    recompute_fov = True
    fov_map = initialize_fov(game_map)

    memory = [[False for y in range(map_height)] for x in range(map_width)]

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        if recompute_fov:
            compute_fov(fov_map, memory, player.x, player.y, fov_radius)

        render_all(console, entities, game_map, fov_map, memory, screen_width, screen_height)
        libtcod.console_flush()
        libtcod.sys_wait_for_event(libtcod.EVENT_KEY_PRESS, key, mouse, True)
        clear_all(console, entities)

        recompute_fov = False

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if player.move(dx, dy, game_map):
                recompute_fov = True

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
