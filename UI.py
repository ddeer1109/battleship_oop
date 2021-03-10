from time import sleep

from board_objects.consts import MISS, HIT, SUNK
from os import system, name


class UI:
    @staticmethod
    def clear_console():
        """Clears console."""
        if name == "nt":
            _ = system("cls")
        else:
            _ = system("clear")

    @staticmethod
    def shotting_turn(pl_object):
        UI.clear_console()
        print(f"\n{pl_object.nickname} turn.\n")

        player_board = pl_object.player_bd.get_printable_list()
        opponent_board = pl_object.opp_copy_bd.get_printable_list()
        center_value = len(player_board[0]) + 6
        print(f"{'Your board:'.center(center_value)}" + f"{'Opponent board:'.center(center_value)}")
        for index in range(len(player_board)):
            pass
            print(f"{player_board[index].center(center_value)}" + f"{opponent_board[index].center(center_value)}")
        sleep(1.5)

    @staticmethod
    def display_feedback_after_shot(result_of_shot, shot):
        """Display adequate communicate after shot made on given coordinates."""
        if result_of_shot == HIT:
            message = "You hitted the ship. Try to hit next one!"
        elif result_of_shot == MISS:
            message = "You missed."
        elif result_of_shot == SUNK:
            message = "You've sunk enemy ship."
        elif result_of_shot == "M_repeat":
            message = "You have tryed this already! Try other coords!"
        print(f"At ({shot.x}, {shot.y}) {message}", end="")

    @staticmethod
    def finish_placing_turn(player_object):
        UI.clear_console()
        print(f"{player_object.nickname} placing turn finished")
        for row in player_object.player_bd.get_printable_list():
            print(row)
        input("Press enter to continue")

    @staticmethod
    def placing_turn(player_object, ship_length):
        sleep(0.5)
        UI.clear_console()
        print(f"{player_object.nickname} placing turn")
        for row in player_object.player_bd.get_printable_list():
            print(row)
        print(f"Placing ship with length: {ship_length}.")

    @staticmethod
    def present_winner(p_object, opp_object):
        UI.clear_console()
        print(f"\nWinner is {p_object.nickname}")

        player_board = p_object.player_bd.get_printable_list()
        opponent_board = opp_object.player_bd.get_printable_list()
        print(f"{'Winner board: '.center(20)}" + f"{'Defeated board:'.center(20)}")
        for index in range(len(player_board)):
            print(f"{player_board[index].center(20)}" + f"{opponent_board[index].center(20)}")
        sleep(0.5)