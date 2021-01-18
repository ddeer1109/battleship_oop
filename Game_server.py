EMPTY_SYMBOL = "."
SHIP_SYMBOL = "X"
HIT_SYMBOL = "H"
SUNK_SYMBOL = "S"
MISSED_SYMBOL = "M"
SHIPS_LENGTHS_FOR_BOARD_SIZES = {
        5: [3,2,2,1],
        6: [3,2,2,2],
        7: [3,3,2,2],
        8: [4,3,3,2],
        9: [4,3,3,2,2],
        10: [4,3,3,3,2,2]
        }

from Player import AI_player, Human_player
from Placing import service_placing
from Shooting import service_shooting_phase, clear_console


def start_game(size_of_board=5, turns_limit=None):
    
    player1 = AI_player("Player1", size_of_board)
    player2 = AI_player("Player2", size_of_board)
    
    service_placing(player1, SHIPS_LENGTHS_FOR_BOARD_SIZES[size_of_board])
    service_placing(player2, SHIPS_LENGTHS_FOR_BOARD_SIZES[size_of_board])
    
    winner, defeated = service_shooting_phase(player1, player2, turns_limit)

    present_winner(winner, defeated)


def main_menu():
    print("Welcome in battleships. ")
    map_size = choose_map_size()
    turns_limit = choose_turns_limit()
    start_game(map_size, turns_limit)


def choose_turns_limit():
    user_input = input("Specify turns limit 20-40 or leave blank to set no limit: ")
    up_limit, down_limit = 40,20
    

    if user_input == "":
        return None
    return int(user_input) if int(user_input) < up_limit and int(user_input) > down_limit else None


def choose_map_size():
    try:
        user_choice = int(input("Map size 5-10: "))
        return user_choice if user_choice in SHIPS_LENGTHS_FOR_BOARD_SIZES.keys() else 5
    except:
        return 5


def present_winner(p_object, opp_object):
    clear_console()
    print(f"Winner is {p_object.nickname}")
    
    print("Winners board:")
    p_object.p_board.print()
    
    print()
    
    print("Defeated board:")
    opp_object.p_board.print()