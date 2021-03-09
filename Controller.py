from time import sleep

from InputGetter import InputGetter
from UI import UI
from board_objects.Board import Board
from board_objects.Placing import Placing
from board_objects.consts import MISS, EMPTY, SHIP, MISS_AGAIN, HIT, SUNK
from board_objects.Field import Field


class Controller:

    def __init__(self, player1, player2, map_size=5):
        self.player1 = player1
        self.player1.set_empty_boards(map_size, map_size)
        self.player2 = player2
        self.player2.set_empty_boards(map_size, map_size)

        InputGetter.LENGTH_DICT, InputGetter.WIDTH_DICT = InputGetter.create_coords_translation_dictionary()
        self.winner = None
        self.defeated = None

    @staticmethod
    def service_placing(player_object, ships_lengths_list):
        human_player = player_object.ishuman

        for ship_length in ships_lengths_list:

            UI.placing_turn(player_object, ship_length)

            is_placing_invalid = True
            while is_placing_invalid:
                # if human_player:
                #     coord1 = InputGetter.get_user_valid_coord()
                #     coord2 = InputGetter.get_user_valid_coord()
                # else:

                coord1, coord2 = InputGetter.get_AI_valid_coords(player_object.player_bd, ship_length)
                sleep(0.5)

                placing = Placing(coord1, coord2)
                is_placing_invalid = not placing.is_correct(player_object.player_bd, ship_length)
                # if is_placing_invalid and human_player:
                #     print("Invalid coordinates.")

            placing.place_ship(player_object.player_bd, ship_length, player_object.ships)
            # clear_console()
        UI.finish_placing_turn(player_object)
        # clear_console()

    def service_shooting_phase(self, p1_obj, p2_obj, turns_limit=None):

        turns_counter = turns_limit

        current_player = p1_obj
        current_opponent = p2_obj

        while self.winner is None and turns_counter != 0:

            self.process_turn_of_player(current_player, current_opponent)

            if turns_limit is not None:
                print(f"Turns left: {turns_counter}")
                turns_counter -= 1

            current_player = p2_obj if current_player is p1_obj else p1_obj
            current_opponent = p1_obj if current_opponent is p2_obj else p2_obj

        return self.winner, self.defeated

    def process_turn_of_player(self, pl_object, opp_p_object):
        """Service one full turn of player, consistning while-looped getting coordinates to shot,
        displaying feedback and checking for win until miss. """
        shot_result = ""
        while shot_result != MISS:

            UI.shotting_turn(pl_object)

            if pl_object.ishuman:
                player_shot = InputGetter.get_user_valid_coord()
            else:
                player_shot = InputGetter.get_AI_shot_coord(pl_object)

            if type(player_shot) is tuple:
                player_shot = Field(player_shot)
            shot_result = Controller.process_shot(player_shot, pl_object, opp_p_object)

            UI.display_feedback_after_shot(shot_result, player_shot)

            if Controller.has_won(opp_p_object.ships):
                self.winner = pl_object
                self.defeated = opp_p_object

    @staticmethod
    def process_shot(player_shot, pl_object, opp_p_object):
        state_of_shot_field = opp_p_object.player_bd.get_field(player_shot.x, player_shot.y).state

        if state_of_shot_field == EMPTY:
            shot_result = MISS
        elif state_of_shot_field == MISS:
            shot_result = MISS_AGAIN
        elif state_of_shot_field == SHIP:
            shot_result = HIT

        if shot_result in [MISS, HIT]:
            pl_object.opp_copy_bd.get_field(player_shot.x, player_shot.y).set_state(shot_result)
            pl_object.shots_stats[(player_shot.x, player_shot.y)] = shot_result

            if shot_result == HIT:
                opp_p_object.player_bd.get_field(player_shot.x, player_shot.y).set_state(shot_result)
                ship = opp_p_object.ships.get_ship_by_part((player_shot.x, player_shot.y))

                if not pl_object.ishuman:
                    pl_object.shots_stats[(player_shot.x, player_shot.y)] = HIT

                ship.update_sunk_state()

                if ship.sunk:
                    for part_key in ship.parts.keys():
                        pl_object.shots_stats[part_key] = SUNK
                        pl_object.opp_copy_bd.get_field(part_key[0], part_key[1]).set_state(SUNK)
                    shot_result = SUNK

        return shot_result

    @staticmethod
    def has_won(enemy_ships_list):

        for ship in enemy_ships_list.fleet:
            if ship.not_sunk():
                return False

        return True
