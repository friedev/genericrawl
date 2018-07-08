from libtcodpy import Color


class Tile:
    """
    A tile on a src.map. It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, color, blocks, blocks_sight=None, memory_color=None):
        self.color = color
        self.blocks = blocks

        # By default, if a tile is blocked, it also blocks sight
        if not blocks_sight:
            blocks_sight = blocks

        self.blocks_sight = blocks_sight

        if not memory_color:
            memory_color = color.__sub__(Color(32, 32, 32))

        self.memory_color = memory_color
