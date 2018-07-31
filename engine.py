from color_schemes import ColorSchemes, init_color_schemes
from components.container import Container
from components.fighter import Fighter
from components.sight import Sight
from entity import Entity
from fov import *
from game_messages import MessageLog, Message
from game_states import GameStates
from input import InputSchemes, handle_mouse
from map.game_map import GameMap
from map.tile import Tiles
from render import render_all, clear_all, RenderOrder, name_entities


def get_mouse_tile(console_width, console_height, player_x, player_y, mouse_x, mouse_y):
    center_x = int(console_width / 2)
    center_y = int(console_height / 2)

    mouse_dx = mouse_x - center_x
    mouse_dy = mouse_y - center_y

    mouse_tile_x = mouse_dx + player_x
    mouse_tile_y = mouse_dy + player_y

    return mouse_tile_x, mouse_tile_y


def move_cursor(key_cursor, dx, dy):
    return key_cursor[0] + dx, key_cursor[1] + dy


def main():
    init_color_schemes()

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
    map_width = 65
    map_height = 65

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, 'GeneriCrawl', False)
    console = libtcod.console_new(screen_width, screen_height)
    panel = libtcod.console_new(panel_width, panel_height)
    message_log = MessageLog(message_x, message_width, message_height)

    input_scheme = InputSchemes.VI.value
    color_scheme = ColorSchemes.SOLID.value

    restart = True
    while restart:
        restart = play_game(console, panel, bar_width, message_log, map_width, map_height, input_scheme, color_scheme)


def play_game(console, panel, bar_width, message_log, map_width, map_height, input_scheme, color_scheme):
    game_map = GameMap(map_width, map_height, 1)
    player_sight = Sight()
    player_fighter = Fighter(hp=40, defense=2, power=5)
    player_container = Container(26)
    player = Entity(*game_map.find_open_tile(tile_type=Tiles.ROOM_FLOOR), '@', libtcod.white, 'player',
                    render_order=RenderOrder.PLAYER, sight=player_sight, fighter=player_fighter,
                    container=player_container)
    game_map.entities.append(player)

    recompute_fov = True
    fov_map = game_map.generate_fov_map()
    memory = [[False for y in range(game_map.height)] for x in range(game_map.width)]

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYER_TURN
    previous_game_state = game_state

    key_cursor = (0, 0)
    menu_selection = 0
    throwing = None

    while not libtcod.console_is_window_closed():
        if recompute_fov:
            player.sight.get_fov_angled(fov_map, memory)

        render_all(console, panel, bar_width, message_log, game_map, player, fov_map, memory, color_scheme,
                   game_state, mouse, menu_selection, key_cursor if game_state is GameStates.TARGETING else None)
        libtcod.console_flush()
        libtcod.sys_wait_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse, True)
        clear_all(console, game_map.entities, player)

        recompute_fov = False

        mouse_action = handle_mouse(mouse)
        action = input_scheme.handle_key(key, game_state)

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        direction = action.get('direction')
        inventory = action.get('inventory')
        pickup = action.get('pickup')
        select = action.get('select')
        drop = action.get('drop')
        use = action.get('use')
        throw = action.get('throw')
        wait = action.get('wait')
        restart = action.get('restart')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        player_results = {}
        player_acted = False

        do_throw = False

        if left_click:
            if game_state is GameStates.TARGETING:
                key_cursor = get_mouse_tile(libtcod.console_get_width(console), libtcod.console_get_height(
                    console), player.x, player.y, *left_click)
                do_throw = True
            else:
                mouse_tile = get_mouse_tile(libtcod.console_get_width(console), libtcod.console_get_height(
                    console), player.x, player.y, *left_click)
                if libtcod.map_is_in_fov(fov_map, *mouse_tile):
                    entity_list = game_map.get_entities_at_tile(*mouse_tile)
                    if len(entity_list) > 0:
                        entity_names = name_entities(entity_list)
                        message_log.add_message(Message('You see ' + entity_names + '.', libtcod.light_gray))

        if right_click and GameStates.TARGETING:
            game_state = previous_game_state
            throwing = None

        if direction:
            if game_state is GameStates.PLAYER_TURN:
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
                            attack_results = player.fighter.attack(target.fighter)
                            player_results = {**player_results, **attack_results}
                            player_acted = True
                        elif game_map.get_tile(player.x + dx, player.y + dy, value=False) is Tiles.STAIRS:
                            game_map = GameMap(map_width, map_height, game_map.dungeon_level + 1)

                            player.fighter.max_hp += 10
                            player.fighter.hp = player.fighter.max_hp
                            player.x, player.y = game_map.find_open_tile(tile_type=Tiles.ROOM_FLOOR)
                            game_map.entities.append(player)

                            recompute_fov = True
                            fov_map = game_map.generate_fov_map()
                            memory = [[False for y in range(game_map.height)] for x in range(game_map.width)]
                            player_acted = False

                            libtcod.console_clear(console)

            elif game_state is GameStates.INVENTORY:
                dy = direction[1]
                menu_selection += dy
                if menu_selection < 0:
                    menu_selection = len(player.container.items) - 1
                elif menu_selection >= len(player.container.items):
                    menu_selection = 0
            elif game_state is GameStates.TARGETING:
                # Moves the key_cursor in the given direction
                key_cursor = move_cursor(key_cursor, *direction)

        if inventory:
            if game_state is GameStates.INVENTORY:
                game_state = previous_game_state
            elif game_state is GameStates.PLAYER_TURN:
                previous_game_state = game_state
                game_state = GameStates.INVENTORY

        if pickup and game_state is GameStates.PLAYER_TURN:
            entities_at_tile = game_map.get_entities_at_tile(player.x, player.y)
            for entity in entities_at_tile:
                if entity.item:
                    player_results = {**player_results, **player.container.add_item(entity)}
                    player_acted = True
                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))

        if drop and game_state is GameStates.INVENTORY:
            if menu_selection < len(player.container.items):
                item = player.container.items.pop(menu_selection)
                item.x = player.x
                item.y = player.y
                game_map.entities.append(item)
                player_acted = True

        if select and game_state is GameStates.TARGETING:
            do_throw = True

        if use and game_state is GameStates.INVENTORY:
            if menu_selection < len(player.container.items):
                use_results = player.container.items[menu_selection].item.use(player)
                player_results = {**player_results, **use_results}
                player_acted = True

        if throw:
            if game_state is GameStates.INVENTORY:
                if menu_selection < len(player.container.items):
                    throwing = player.container.items[menu_selection].item
                    previous_game_state = GameStates.PLAYER_TURN
                    game_state = GameStates.TARGETING
                    key_cursor = (player.x, player.y)
                    message_log.add_message(Message(
                        'Left-click or navigate to a tile to throw. Right-click or escape to cancel.',
                        libtcod.light_gray))
            elif game_state is GameStates.TARGETING and throwing:
                do_throw = True
                pass

        if wait and game_state is GameStates.PLAYER_TURN:
            player_acted = True

        if restart and game_state is GameStates.PLAYER_DEAD:
            return True

        if exit:
            if game_state is GameStates.INVENTORY:
                game_state = previous_game_state
            elif game_state is GameStates.TARGETING:
                game_state = previous_game_state
                throwing = None
            else:
                return False

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # Process actions with multiple triggers
        if do_throw:
            if (player.x, player.y) != key_cursor and libtcod.map_is_in_fov(fov_map, *key_cursor) and \
                    game_map.is_tile_open(*key_cursor, check_entities=False):
                throw_results = throwing.use(player, throwing=True, target_x=key_cursor[0], target_y=key_cursor[1],
                                             game_map=game_map)
                player_results = {**player_results, **throw_results}
                game_state = previous_game_state
                throwing = None
                player_acted = True

        # Process player turn results
        attack_message = player_results.get('attack_message')
        pickup_message = player_results.get('pickup_message')
        use_message = player_results.get('use_message')
        new_messages = [attack_message, pickup_message, use_message]

        dead_entities = player_results.get('dead')
        item_obtained = player_results.get('item_obtained')
        item_consumed = player_results.get('item_consumed')
        item_moved = player_results.get('item_moved')

        for message in new_messages:
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

        if item_obtained:
            game_map.entities.remove(item_obtained)

        if item_consumed:
            player.container.items.remove(item_consumed)

        if item_moved:
            # Code partially copied from drop
            player.container.items.remove(item_moved)
            item_moved.x = player_results.get('item_x')
            item_moved.y = player_results.get('item_y')

            if item_moved not in game_map.entities:
                game_map.entities.append(item_moved)

        if player_acted:
            game_state = GameStates.ENEMY_TURN

        if game_state is GameStates.ENEMY_TURN:
            enemy_fov_map = game_map.generate_fov_map_with_entities()
            for entity in game_map.entities:
                if entity.ai:
                    enemy_results = entity.ai.act(game_map, player, enemy_fov_map)

                    # Process enemy turn results
                    attack_message = enemy_results.get('attack_message')
                    dead_entities = enemy_results.get('dead')

                    if attack_message:
                        message_log.add_message(attack_message)

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

                if game_state is GameStates.PLAYER_DEAD:
                    break
            else:
                game_state = GameStates.PLAYER_TURN


if __name__ == '__main__':
    main()
