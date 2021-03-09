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
        print(f"{pl_object.nickname} turn.\n")

        print("Your board:")
        pl_object.player_bd.print()
        print("Your copy of opponent board:")
        pl_object.opp_copy_bd.print()
        sleep(0.5)

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
        print(f"{player_object.nickname} placing turn finished")
        player_object.player_bd.print()
        input("Press enter to continue")

    @staticmethod
    def placing_turn(player_object, ship_length):
        UI.clear_console()
        print(f"{player_object.nickname} placing turn")
        player_object.player_bd.print()
        print(f"Placing ship with length: {ship_length}.")

    @staticmethod
    def present_winner(p_object, opp_object):
        UI.clear_console()
        print(f"Winner is {p_object.nickname}")

        print("Winners board:")
        p_object.player_bd.print()

        print()

        print("Defeated board:")
        opp_object.player_bd.print()