from math import radians
from random import randint


def generate_facing():
    return radians(randint(0, 7) * 45)


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    def __init__(self, x, y, char, color, name, facing=generate_facing(), blocks=True, is_name_proper=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.facing = facing
        self.blocks = blocks

        if is_name_proper:
            self.definite_name = name
            self.indefinite_name = name
        else:
            self.definite_name = 'the ' + name
            if name[0].lower() in 'aeiou':
                self.indefinite_name = 'an ' + name
            else:
                self.indefinite_name = 'a ' + name

    def move_to(self, x, y, game_map):
        if game_map.is_tile_open(x, y):
            self.x = x
            self.y = y
            return True
        return False

    def move(self, dx, dy, game_map):
        return self.move_to(self.x + dx, self.y + dy, game_map)

    # This method and the facing field are temporary, and will be replaced by the ECS
    def face(self, facing):
        self.facing = facing
        return True
