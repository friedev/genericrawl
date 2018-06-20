class Tile:
    """
    A tile on a src.map. It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, color, blocked, block_sight=None):
        self.color = color
        self.blocked = blocked

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
