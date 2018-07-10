import libtcodpy as libtcod
from math import atan2

from fov import distance
from render import RenderOrder


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    def __init__(self, x, y, char, color, name, is_name_proper=False, blocks=True, render_order=RenderOrder.CORPSE,
                 sight=None, fighter=None, ai=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.is_name_proper = is_name_proper
        self.blocks = blocks
        self.render_order = render_order
        self.sight = sight
        self.fighter = fighter
        self.ai = ai

        if self.sight:
            self.sight.owner = self

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

    def definite_name(self):
        if self.is_name_proper:
            return self.name
        else:
            return 'the ' + self.name

    def indefinite_name(self):
        if self.is_name_proper:
            return self.name
        else:
            # Chooses the right indefinite article if the name starts with a vowel
            if self.name[0].lower() in 'aeiou':
                return 'an ' + self.name
            else:
                return 'a ' + self.name

    def move_to(self, x, y, game_map, face=False):
        if game_map.is_tile_open(x, y):
            if face and self.sight:
                self.sight.face(atan2(y - self.y, x - self.x))
            self.x = x
            self.y = y
            return True
        return False

    def move(self, dx, dy, game_map, face=True):
        return self.move_to(self.x + dx, self.y + dy, game_map, face)

    def distance_to(self, other):
        return distance(self.x, self.y, other.x, other.y)

    def kill(self, is_player=False):
        self.char = '%'
        self.color = libtcod.dark_red

        if is_player:
            return 'You have died!'
        else:
            # Death message must be set before changing the entity's name to that of its corpse
            death_message = '{0} has died!'.format(self.definite_name().capitalize())

            self.blocks = False
            self.render_order = RenderOrder.CORPSE
            self.fighter = None
            self.ai = None
            if self.is_name_proper:
                self.name = self.name + "'s corpse"
            else:
                self.name = self.name + ' corpse'

            return death_message
