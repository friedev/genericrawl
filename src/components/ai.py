from random import randint

from fov import *


class BasicMonster:
    def act(self, game_map, player, fov_map=None):
        results = {}

        dist = self.owner.distance_to(player)
        given_fov_map = fov_map is not None
        if dist <= self.owner.sight.fov_radius:
            if dist >= 2:
                owner_x = self.owner.x
                owner_y = self.owner.y
                player_x = player.x
                player_y = player.y

                if given_fov_map:
                    libtcod.map_set_properties(fov_map, owner_x, owner_y, True, True)
                    libtcod.map_set_properties(fov_map, player_x, player_y, True, True)
                    use_fov_map = fov_map
                else:
                    # This second variable is necessary as creating another variable called fov_map might shadow the
                    # parameter rather than changing its value
                    use_fov_map = game_map.generate_fov_map_with_entities([self.owner, player])

                # 1.41 approximates sqrt(2), the cost of a diagonal moves
                path = libtcod.path_new_using_map(use_fov_map, 1.41)
                libtcod.path_compute(path, owner_x, owner_y, player_x, player_y)

                if not libtcod.path_is_empty(path) and libtcod.path_size(path) < 25:
                    x, y = libtcod.path_walk(path, True)
                    if x or y:
                        self.owner.move_to(x, y, game_map, face=True)
                else:
                    dx = player_x - owner_x
                    dy = player_y - owner_y

                    dx = int(round(dx / dist))
                    dy = int(round(dy / dist))

                    if game_map.is_tile_open(owner_x + dx, owner_y + dy):
                        self.owner.move(dx, dy, game_map)

                libtcod.path_delete(path)
                if given_fov_map:
                    libtcod.map_set_properties(use_fov_map, self.owner.x, self.owner.y, True, False)
                    libtcod.map_set_properties(use_fov_map, player.x, player.y, True, False)
                else:
                    libtcod.map_delete(use_fov_map)
            else:
                # Add the results of the attack to the existing results
                results = {**results, **self.owner.fighter.attack(player.fighter)}
        else:
            # Update the FOV map if given one
            if given_fov_map:
                libtcod.map_set_properties(fov_map, self.owner.x, self.owner.y, True, True)

            self.owner.move(randint(-1, 1), randint(-1, 1), game_map)

            if given_fov_map:
                libtcod.map_set_properties(fov_map, self.owner.x, self.owner.y, True, False)

        return results
