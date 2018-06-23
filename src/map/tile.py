from libtcodpy import Color


class Tile:
    """
    A tile on a src.map. It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, color, blocked, block_sight=None, memory_color=None):
        self.color = color
        self.blocked = blocked

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

        if memory_color is None:
            memory_color = color.__sub__(Color(32, 32, 32))

        self.memory_color = memory_color
