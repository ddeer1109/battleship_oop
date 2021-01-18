ROW_INDEX = 0
COL_INDEX = 1
SHIPS_STATE_INDEX = 2

import random
import copy
from Board import *
from Placing import Placing
from Shooting import *
from Game_server import EMPTY_SYMBOL, SHIP_SYMBOL, MISSED_SYMBOL, SUNK_SYMBOL, HIT_SYMBOL


class Player:
    def __init__(self, player_nickname, board_size=5):
        self.nickname = player_nickname
        self.p_board = Board(length=board_size, width=board_size)
        self.opp_board_copy = Board(length=board_size, width=board_size)
        self.ships_list = []
        self.is_human_player = True
    
    #shooting

    def process_turn_of_player(self, opp_p_object):
        """Service one full turn of player, consistning while-looped getting coordinates to shot, 
        displaying feedback and checking for win until miss. """
        shot_result = ""
        while shot_result != MISSED_SYMBOL:
            print(f"{self.nickname} turn.\n")
            
            print("Your board:") 
            self.p_board.print()
            print("Your copy of opponent board:") 
            self.opp_board_copy.print()
        
            if self.is_human_player:
                player_shot = self.get_user_valid_coord()
            else:
                player_shot = self.get_AI_shot_coord(opp_p_object.ships_list)

            shot_result = self.process_a_shot(opp_p_object, player_shot[ROW_INDEX], player_shot[COL_INDEX])
            
            display_feedback_after_shot(shot_result, player_shot[ROW_INDEX], player_shot[COL_INDEX])

            if has_won(opp_p_object.ships_list):
                return self, opp_p_object


    def process_a_shot(self, opp_p_object, shot_row, shot_col):
        """Serve whole process of shot for given (shot_row, shot_col) and changes state of field on both of boards"""
        state_of_shotted_field = opp_p_object.p_board.fields[shot_row][shot_col]
        
        if state_of_shotted_field == EMPTY_SYMBOL:
            
            if self.opp_board_copy.fields[shot_row][shot_col] == MISSED_SYMBOL:
                shot_result = "M_repeat"
                return shot_result
            
            shot_result = MISSED_SYMBOL
            self.opp_board_copy.mark_shot_on_board(shot_row, shot_col, shot_result)
        
        elif state_of_shotted_field == SHIP_SYMBOL:
            shot_result = HIT_SYMBOL
            self.opp_board_copy.mark_shot_on_board(shot_row, shot_col, shot_result)
            update_ships_state(shot_row, shot_col, opp_p_object, self)
            
            if is_ship_sunk(shot_row, shot_col, opp_p_object):
                shot_result = SUNK_SYMBOL
        
        return shot_result



class Human_player(Player, Board):
    def get_user_valid_coord(self):
        """Gets single, validated coordinate of player. In this version 'A-J1-10' supported.""" 
        correct_ROWS = self.p_board.LENGTH_DICT.keys()
        correct_COLS = self.p_board.WIDTH_DICT.keys()
        
        user_input = str.upper(input("Your coordinate:"))
        input_length_not_correct = len(user_input) < 2 or len(user_input) > 3 
        
        while input_length_not_correct:
            print("Incorrect input.")
            user_input = str.upper(input("Try again: "))     
            input_length_not_correct = len(user_input) < 2 or len(user_input) > 3

        input_is_not_correct = user_input[0] not in correct_ROWS or user_input[1:] not in correct_COLS
        
        while input_is_not_correct:
            print("Incorrect input.")
            user_input = str.upper(input("Try again: "))
            input_is_not_correct = user_input[0] not in correct_ROWS or user_input[1:] not in correct_COLS
        
        return self.translate_user_coords(user_input)


    def translate_user_coords(self, coordinate):
        row, col = self.p_board.LENGTH_DICT[coordinate[0]], self.p_board.WIDTH_DICT[coordinate[1]]
        return (row, col)


class AI_player(Player):
    def __init__(self, player_nickname, board_size=5):
        self.nickname = player_nickname
        self.p_board = Board(length=board_size, width=board_size)
        self.opp_board_copy = Board(length=board_size, width=board_size)
        self.ships_list = []
        self.is_human_player = False

    #placing
    def get_AI_valid_coords(self, ship_length):
        """Returns random placing coords in correct order. Help function for AI placing."""
        empty_fields = self.p_board.get_empty_fields()
        row1, col1 = random.choice(empty_fields)
        move_in_orientation = random.choice(["row", "col"])

        modified_field = col1 if move_in_orientation == "row" else row1

        if modified_field + ship_length > len(self.p_board.fields[0]):
            modified_field -= ship_length - 1            
        else:
            modified_field += ship_length - 1
        
        if move_in_orientation == "row":
            return (row1, min(col1, modified_field)), (row1, max(col1, modified_field))      
        else:
            return (min(row1, modified_field), col1), (max(row1, modified_field), col1)    


    #shooting
    def get_AI_shot_coord(self, opponent_ships):
        """Wrapper for AI shooting. Gets list of already hit fields, if its empty returns random shot. 
        If its not iterates over hit fields and over its neighbours in purpose to get another succesful shots.
        It does not check neighbours which are neighbours for sunk ships (SUNK_SYMBOL), as they cannot contain another ship's parts
        In this version if there are two hit fields it only seeks for third in neighbours with same orientation"""
        hit_fields = get_hit_fields(opponent_ships)
        if len(hit_fields) == 0: return random.choice(self.opp_board_copy.get_empty_fields())

        for hit in hit_fields:
            
            neighs = [neigh for neigh in self.get_neighs_of_shot(hit) if neigh != None and
             self.opp_board_copy.fields[neigh[ROW_INDEX]][neigh[COL_INDEX]] == EMPTY_SYMBOL]
            
            for neigh in neighs:

                row, col = neigh[ROW_INDEX], neigh[COL_INDEX]
                shot_placing = Placing((row,col), (row,col))
                
                neigh_is_not_ship = SUNK_SYMBOL not in shot_placing.get_neighbours(self.opp_board_copy.fields, ship_length=1)
                
                if len(hit_fields) == 2 and neigh_is_not_ship:
                    
                    hits_orientation = ROW_INDEX if hit_fields[0][ROW_INDEX] == hit_fields[1][ROW_INDEX] else COL_INDEX
                    
                    if neigh[hits_orientation] != hit[hits_orientation]: 
                        continue

                    right_shots = [neigh for neigh in neighs if neigh[hits_orientation] == hit[hits_orientation]]
                    return random.choice(right_shots)
                
                if neigh_is_not_ship:  
                    return neigh


    def get_neighs_of_shot(self, hit):
        """Get neighbour coords for given hit coords. Help function for AI shooting."""
        upper = (hit[ROW_INDEX]+1, hit[COL_INDEX]) if hit[ROW_INDEX]+1 < len(self.opp_board_copy.fields) else None
        right = (hit[ROW_INDEX], hit[COL_INDEX]+1) if hit[COL_INDEX]+1 < len(self.opp_board_copy.fields[ROW_INDEX]) else None
        lower = (hit[ROW_INDEX]-1, hit[COL_INDEX]) if hit[ROW_INDEX]-1 >= 0 else None
        left = (hit[ROW_INDEX], hit[COL_INDEX]-1) if hit[COL_INDEX]-1 >= 0 else None

        return lower, right, upper, left



def get_hit_fields(opponent_ships):
    """Get coords of already hit fields. Help function for AI shooting."""
    hit_fields_coords_list = []

    for ship in opponent_ships:
        for part in ship:
            if ship [part] == HIT_SYMBOL: 
                hit_fields_coords_list.append(part)

    return hit_fields_coords_list


