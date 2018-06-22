class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move_to(self, x, y, game_map):
        if 0 <= x < game_map.width and 0 <= y < game_map.height and not game_map.get_tile(x, y).blocked:
            self.x = x
            self.y = y

    def move(self, dx, dy, game_map):
        self.move_to(self.x + dx, self.y + dy, game_map)
