ROW_INDEX = 0
COL_INDEX = 1

from Player import *
from os import system, name
from time import sleep
from Game_server import EMPTY_SYMBOL, SHIP_SYMBOL, HIT_SYMBOL, SUNK_SYMBOL, MISSED_SYMBOL

def clear_console():
    """Clears console."""
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


def service_shooting_phase(p1_obj, p2_obj, turns_limit):
    winner_after_turn = None
    turns_counter = turns_limit

    current_player = p1_obj
    current_opponent = p2_obj
    
    while winner_after_turn == None and turns_counter != 0:
        

        winner_after_turn = serve_turn_of_player(current_player, current_opponent)
        
        if turns_limit != None: 
            print(f"Turns left: {turns_counter}")
            turns_counter -= 1

        current_player = p2_obj if current_player is p1_obj else p1_obj 
        current_opponent = p1_obj if current_opponent is p2_obj else p2_obj
             
    return winner_after_turn


def is_ship_sunk(row_index, column_index, player_object):
    """Checks if ship which contain part of given coords is sunk."""
    for ship in player_object.ships_list:
        if (row_index, column_index) in ship and SHIP_SYMBOL not in ship.values():
            return True
    return False


def update_ships_state(row_index, column_index, opp_p_object, p_object):
    """Update state of ships. It contains changing ships state for sunk."""

    enemy_ships = opp_p_object.ships_list
    
    for ship_num in range(len(enemy_ships)):
        
        for coords, state in enemy_ships[ship_num].items():

            if row_index == coords[ROW_INDEX] and column_index == coords[COL_INDEX]:
                enemy_ships [ship_num] [coords] = HIT_SYMBOL

        states_of_ship = enemy_ships[ship_num].values()
        all_ships_part_hit = SHIP_SYMBOL not in states_of_ship
        
        if all_ships_part_hit:
            
            for part_of_ship_coord in enemy_ships[ship_num]:
                enemy_ships[ship_num][part_of_ship_coord] = SUNK_SYMBOL
            
            drown_ship_on_board(p_object, opp_p_object, ship_num)


def drown_ship_on_board(p_object, opp_p_object, ship_num):
    """Changes state for sunk (SUNK_SYMBOL) of ship with all parts hit on both of boards"""
    
    for part in opp_p_object.ships_list[ship_num].keys():
        
        p_object.opp_board_copy.mark_shot_on_board(part[ROW_INDEX], part[COL_INDEX], SUNK_SYMBOL)
        
        opp_p_object.p_board.mark_shot_on_board(part[ROW_INDEX], part[COL_INDEX], SUNK_SYMBOL)


def display_feedback_after_shot(result_of_shot, shot_row, shot_col):
    """Display adequate communicate after shot made on given coordinates."""
    if result_of_shot == HIT_SYMBOL:
        message = "You hitted the ship. Try to hit next one!"
    elif result_of_shot == MISSED_SYMBOL:
        message = "You missed."
    elif result_of_shot == SUNK_SYMBOL:
        message = "You've sunk enemy ship."
    elif result_of_shot == "M_repeat":
        message = "You have tryed this already! Try other coords!"
    print(f"At ({shot_row}, {shot_col}) {message}", end="")
    sleep(1)
    clear_console()


def has_won(enemy_ships_list):
    for ship in enemy_ships_list:
        if SHIP_SYMBOL in ship.values():
            return False

    return True


def serve_turn_of_player(p_object, opp_object):
    
    result_of_turn = p_object.process_turn_of_player(opp_object)

    return result_of_turn
