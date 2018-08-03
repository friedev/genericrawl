import libtcodpy as libtcod
from random import randint


class BasicMonster:
    def __init__(self, clairvoyant=False, chase_duration=5):
        self.clairvoyant = clairvoyant
        self.chase_duration = chase_duration
        self.remaining_chase_turns = 0

    def act(self, game_map, player, fov_map=None, has_los=None):
        dist = self.owner.distance_to(player)

        if dist < 2:
            # Attack the player, even if the entity can't see
            return self.owner.fighter.attack_entity(player.fighter)

        results = {}
        given_fov_map = fov_map is not None

        if self.owner.sight and dist <= self.owner.sight.fov_radius or self.remaining_chase_turns > 0:
            owner_x = self.owner.x
            owner_y = self.owner.y
            player_x = player.x
            player_y = player.y

            if given_fov_map:
                libtcod.map_set_properties(fov_map, owner_x, owner_y, True, True)
                libtcod.map_set_properties(fov_map, player_x, player_y, True, True)
            else:
                # This second variable is necessary as creating another variable called fov_map might shadow the
                # parameter rather than changing its value
                fov_map = game_map.generate_fov_map_with_entities([self.owner, player])

            if self.clairvoyant:
                # Clairvoyant entities can always sense the player when they're nearby
                has_los = True

            if has_los is None:
                self.owner.sight.get_fov(fov_map)
                has_los = libtcod.map_is_in_fov(fov_map, owner_x, owner_y)

            if has_los:
                # If the entity can see the player, reset the chase timer
                self.remaining_chase_turns = self.chase_duration

            chase = has_los

            if not has_los and self.remaining_chase_turns > 0:
                # Entities will continue chasing the player for chase_duration, even if they don't have line of sight
                chase = True
                self.remaining_chase_turns -= 1

            if chase:
                # 1.41 approximates sqrt(2), the cost of a diagonal moves
                path = libtcod.path_new_using_map(fov_map, 1.41)
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
                libtcod.map_set_properties(fov_map, self.owner.x, self.owner.y, True, False)
                libtcod.map_set_properties(fov_map, player.x, player.y, True, False)
            else:
                libtcod.map_delete(fov_map)
        else:
            if given_fov_map:
                # Remove the entity from the given FOV map
                libtcod.map_set_properties(fov_map, self.owner.x, self.owner.y, True, True)

            # Wander around aimlessly
            self.owner.move(randint(-1, 1), randint(-1, 1), game_map)

            if given_fov_map:
                # Add the entity to the given FOV map
                libtcod.map_set_properties(fov_map, self.owner.x, self.owner.y, True, False)

        return results
