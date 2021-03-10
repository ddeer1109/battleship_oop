from Controller import Controller
from UI import UI
from Player import Player

SHIPS_LENGTHS_FOR_BOARD_SIZES = {
        5: [3,2,1],
        6: [3,2,2,2],
        7: [4,3,3,2,2],
        8: [4,3,3,2],
        9: [4,3,3,2,2],
        10: [4,3,3,3,2,2]
        }


class GameServer:
    def __init__(self, preset=False):
        if not preset:
            self.player1 = GameServer.get_player()
            self.player2 = GameServer.get_player()
            self.map_size = self.choose_map_size()
            self.turns_limit = self.choose_turns_limit()
        else:
            self.player1 = Player("PLAYER 1", ishuman=False)
            self.player2 = Player("PLAYER 2", ishuman=False)
            self.map_size = 7
            self.turns_limit = None

    def start_game(self):
        controller = Controller(self.player1, self.player2, self.map_size)

        controller.service_placing(
            self.player1,
            SHIPS_LENGTHS_FOR_BOARD_SIZES[self.map_size])

        controller.service_placing(
            self.player2,
            SHIPS_LENGTHS_FOR_BOARD_SIZES[self.map_size])

        winner, defeated = controller.service_shooting_phase(
            self.player1,
            self.player2,
            self.turns_limit)

        UI.present_winner(winner, defeated)

    @staticmethod
    def choose_turns_limit():
        user_input = input("Specify turns limit 20-40 or leave blank to set no limit: ")
        up_limit, down_limit = 40,20

        if user_input == "":
            return None
        return int(user_input) if int(user_input) < up_limit and int(user_input) > down_limit else None

    @staticmethod
    def choose_map_size():
        try:
            user_choice = int(input("Map size 5-10: "))
            return user_choice if user_choice in SHIPS_LENGTHS_FOR_BOARD_SIZES.keys() else 5
        except:
            return 5

    @staticmethod
    def get_player():
        nickname = input("Choose player 1 nickname: ")
        print()
        is_human = "y" in input("Is human player?\ny for human, n for ai: ").lower()

        return Player(nickname, is_human)


