from color_schemes import ColorSchemes
from src.components.fighter import Fighter
from src.components.sight import Sight
from src.entity import Entity
from src.fov import *
from src.game_messages import MessageLog
from src.game_states import GameStates
from src.input import handle_keys
from src.map.game_map import GameMap
from src.render import render_all, clear_all, RenderOrder


def main():
    # Screen dimensions, in characters
    screen_width = 80
    screen_height = 50

    # Panel dimensions, in characters
    panel_width = screen_width
    panel_height = 7

    # Health bar dimensions, in characters
    bar_width = 20

    # Message box dimensions, in characters
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    # Map dimensions, in tiles
    map_width = 100
    map_height = 100

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, 'GeneriCrawl', False)
    console = libtcod.console_new(screen_width, screen_height)
    panel = libtcod.console_new(panel_width, panel_height)

    message_log = MessageLog(message_x, message_width, message_height)

    restart = True
    while restart:
        restart = play_game(console, panel, bar_width, message_log, map_width, map_height)


def play_game(console, panel, bar_width, message_log, map_width, map_height):
    game_map = GameMap(map_width, map_height)
    player_sight = Sight()
    player_fighter = Fighter(hp=30, defense=2, power=5)
    player = Entity(*game_map.find_open_tile(), '@', libtcod.white, 'player', render_order=RenderOrder.PLAYER,
                    sight=player_sight, fighter=player_fighter)
    game_map.entities.append(player)

    recompute_fov = True
    fov_map = game_map.generate_fov_map()
    memory = [[False for y in range(0, game_map.height)] for x in range(0, game_map.width)]
    color_scheme = ColorSchemes.SOLID.value

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYER_TURN

    while not libtcod.console_is_window_closed():
        if recompute_fov:
            player.sight.get_fov_angled(fov_map, memory)

        render_all(console, panel, bar_width, message_log, game_map, player, fov_map, memory, color_scheme, mouse)
        libtcod.console_flush()
        libtcod.sys_wait_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse, True)
        clear_all(console, game_map.entities, player)

        recompute_fov = False

        action = handle_keys(key)

        direction = action.get('direction')
        wait = action.get('wait')
        restart = action.get('restart')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        player_results = {}

        if game_state == GameStates.PLAYER_TURN:
            player_acted = False

            if direction:
                move = action.get('move')
                face = action.get('face')
                dx, dy = direction

                if face and player.sight.face(atan2(dy, dx)):
                    player_acted = True
                    recompute_fov = True

                if move:
                    if player.move(dx, dy, game_map, face=False):
                        player_acted = True
                        recompute_fov = True
                    else:
                        blocking_entities = game_map.get_entities_at_tile(player.x + dx, player.y + dy, True)
                        if blocking_entities:
                            target = blocking_entities[0]
                            # Add the results of the attack to the existing results
                            player_results = {**player_results, **player.fighter.attack(target.fighter)}
                            player_acted = True

            if wait:
                player_acted = True

            if player_acted:
                game_state = GameStates.ENEMY_TURN

        if restart and game_state == GameStates.PLAYER_DEAD:
            return True

        if exit:
            return False

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # Process player turn results
        message = player_results.get('message')
        dead_entities = player_results.get('dead')

        if message:
            message_log.add_message(message)

        if dead_entities:
            for dead_entity in dead_entities:
                if dead_entity == player:
                    message = player.kill(is_player=True)
                    game_state = GameStates.PLAYER_DEAD
                else:
                    message = dead_entity.kill()
                message_log.add_message(message)

        if game_state == GameStates.ENEMY_TURN:
            enemy_fov_map = game_map.generate_fov_map_with_entities()
            for entity in game_map.entities:
                if entity.ai:
                    enemy_results = entity.ai.act(game_map, player, enemy_fov_map)

                    # Process enemy turn results
                    message = enemy_results.get('message')
                    dead_entities = enemy_results.get('dead')

                    if message:
                        message_log.add_message(message)

                    if dead_entities:
                        for dead_entity in dead_entities:
                            if dead_entity == player:
                                message = player.kill(is_player=True)
                                message_log.add_message(message)
                                game_state = GameStates.PLAYER_DEAD
                                break
                            else:
                                message = dead_entity.kill()
                                message_log.add_message(message)

                if game_state == GameStates.PLAYER_DEAD:
                    break
            else:
                game_state = GameStates.PLAYER_TURN


if __name__ == '__main__':
    main()
