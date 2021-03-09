from board_objects.ShipsFleet import Ships
from board_objects.consts import EMPTY, SHIP, MISS, SUNK, HIT
from board_objects.Board import Board
ROW_INDEX = 0
COL_INDEX = 1
SHIPS_STATE_INDEX = 2

# from board_objects.Shooting import *

PLAYER_BD = "p_board"
OPP_COPY_BD = "opp_copy"

class Player:
    def __init__(self, player_nickname, ishuman=True):
        self.nickname = player_nickname
        self.ishuman = ishuman

        self.player_bd = None
        self.opp_copy_bd = None

        self.ships = Ships()
        self.shots_stats = {}

    def __repr__(self):
        return self.nickname

    def set_empty_boards(self, length, width):
        self.player_bd = Board(length, width)
        self.opp_copy_bd = Board(length, width)

    def get_hits(self):
        return [field for field in self.shots_stats.keys() if self.shots_stats[field] == HIT]

    def get_misses(self):
        return [field for field in self.shots_stats.keys() if self.shots_stats[field] == MISS]
