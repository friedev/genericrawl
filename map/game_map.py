class GameMap:
    def __init__(self, width, height, floor, wall):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles(floor, wall)

    def initialize_tiles(self, floor, wall):
        tiles = [[floor for y in range(self.height)] for x in range(self.width)]

        tiles[30][22] = wall
        tiles[31][22] = wall
        tiles[32][22] = wall

        return tiles
