from math import radians
from src.entity import Entity
from src.fov import *
from src.game_states import GameStates
from src.input import handle_keys
from src.map.game_map import GameMap
from src.render import render_all, clear_all


def main():
    # Size of the screen, in tiles
    screen_width = 80
    screen_height = 50

    # Size of the map, in tiles
    map_width = 100
    map_height = 100

    # The maximum number of tiles that can be seen in any direction, in tiles
    fov_radius = 10

    # The total span of the cone of vision, in radians
    fov_span = radians(140)

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, 'GeneriCrawl', False)
    console = libtcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    player = Entity(*game_map.find_open_tile(), '@', libtcod.white, 'you', is_name_proper=True)
    game_map.entities.append(player)

    recompute_fov = True
    fov_map = initialize_fov(game_map)
    memory = []

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    clear_all(console, game_map.entities, player.x, player.y, screen_width, screen_height)

    game_state = GameStates.PLAYER_TURN

    while not libtcod.console_is_window_closed():
        if recompute_fov:
            fov = compute_fov_angled(fov_map, player.x, player.y, fov_radius, player.facing, fov_span)
            update_memory(memory, fov)

        render_all(console, game_map.entities, game_map, fov, memory, player.x, player.y, screen_width, screen_height)
        libtcod.console_flush()
        libtcod.sys_wait_for_event(libtcod.EVENT_KEY_PRESS, key, mouse, True)
        clear_all(console, game_map.entities, player.x, player.y, screen_width, screen_height)

        recompute_fov = False

        action = handle_keys(key)

        direction = action.get('direction')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if direction and game_state == GameStates.PLAYER_TURN:
            move = action.get('move')
            face = action.get('face')
            dx, dy = direction

            player_acted = False

            if face and player.face(atan2(dy, dx)):
                player_acted = True
                recompute_fov = True

            if move:
                if player.move(dx, dy, game_map):
                    player_acted = True
                    recompute_fov = True
                else:
                    blocking_entities = game_map.get_entities_at_tile(player.x + dx, player.y + dy, True)
                    for entity in blocking_entities:
                        # TODO add combat here
                        game_map.entities.remove(entity)
                        player_acted = True

            if player_acted:
                game_state = GameStates.ENEMY_TURN

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        if game_state == GameStates.ENEMY_TURN:
            for entity in game_map.entities:
                if entity != player:
                    # TODO add enemy actions
                    continue

            game_state = GameStates.PLAYER_TURN


if __name__ == '__main__':
    main()
