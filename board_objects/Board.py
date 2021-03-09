import string
import copy
from board_objects.consts import EMPTY
from board_objects.Field import Field


class Board:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.fields= self.init_board()

    def init_board(self):
        board = []

        for i in range(self.length):
                board.append([Field((i, j), state=EMPTY) for j in range(self.width)])
        return board

    def print(self):
        print("".ljust(4) + " ".join([str(number) for number in range(1, self.width+1)]) + "\n")
    
        for row_number, row in enumerate(self.fields):
            print(string.ascii_uppercase[row_number].ljust(3) + " " + " ".join(list(map(str, row))))

    def get_field(self, x_cd, y_cd):
        return self.fields[x_cd][y_cd]

    def set_object_on_board(self, object):
        self.fields[object.x][object.y] = object

    def get_fields_by_type(self, type=EMPTY):
        """Get empty fields of player board. Help function for AI placing"""
        empty_fields_list = []

        for row in self.fields:
            for field in row:
                if field.state == type:
                    empty_fields_list.append(field)

        return empty_fields_list


