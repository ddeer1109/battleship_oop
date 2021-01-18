import string
import copy
from Game_server import EMPTY_SYMBOL
class Board:
    def __init__(self, length, width, board_for_human=True):
        self.length = length
        self.width = width
        self.fields= self.init_board()
        if board_for_human:
            self.LENGTH_DICT, self.WIDTH_DICT = self.create_coords_translation_dictionary()


    def init_board(self):
        board = []
        for i in range(self.length):
            board.append([EMPTY_SYMBOL] * self.width)
        return board


    def print(self):
        print("".ljust(4) + " ".join([str(number) for number in range(1, self.width+1)]) + "\n")
    
        for row_number, row in enumerate(self.fields):
            print(string.ascii_uppercase[row_number].ljust(3) + " " + " ".join(row))

    
    def create_coords_translation_dictionary(self):
        letters = string.ascii_uppercase
        rows_dictionary = dict()
        columns_dictionary = dict()
        
        for length_number in range(self.length):
            rows_dictionary[letters[length_number]] = length_number
        
        for width_number in range(self.width):
            columns_dictionary[str(width_number+1)] = width_number
        
        return rows_dictionary, columns_dictionary
    

    def mark_shot_on_board(self, row_index, col_index, shot_result):
        """Mark shot with given shot result on given board."""
        self.fields[row_index][col_index] = shot_result


    def get_empty_fields(self):
        """Get empty fields of player board. Help function for AI placing"""
        empty_fields_list = []
        for row_index in range(len(self.fields)):
            for col_index in range(len(self.fields[0])):
                if self.fields[row_index][col_index] == EMPTY_SYMBOL:
                    empty_fields_list.append((row_index,col_index))
        return empty_fields_list





