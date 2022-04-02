from enum import Enum, auto


class GameStates(Enum):
    PLAYER_TURN = auto()
    ENEMY_TURN = auto()
    INVENTORY = auto()
    TARGETING = auto()
    PLAYER_DEAD = auto()
    VICTORY = auto()
