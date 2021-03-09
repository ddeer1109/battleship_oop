import random
import string

from board_objects.consts import HIT, SUNK
from board_objects.Field import Field


class InputGetter:

    @staticmethod
    def get_AI_valid_coords(owned_board, ship_length):
        """Returns random placing coords in correct order. Help function for AI placing."""
        empty_fields = owned_board.get_fields_by_type()
        random_field = random.choice(empty_fields)
        row1, col1 = random_field.x, random_field.y
        move_in_orientation = random.choice(["row", "col"])

        modified_field = col1 if move_in_orientation == "row" else row1

        if modified_field + ship_length > len(owned_board.fields[0]):
            modified_field -= ship_length - 1
        else:
            modified_field += ship_length - 1

        if move_in_orientation == "row":
            return Field((row1, min(col1, modified_field))), Field((row1, max(col1, modified_field)))
        else:
            return Field((min(row1, modified_field), col1)), Field((max(row1, modified_field), col1))

    @staticmethod
    def get_user_valid_coord():
        """Gets single, validated coordinate of player. In this version 'A-J1-10' supported."""
        correct_ROWS = InputGetter.LENGTH_DICT.keys()
        correct_COLS = InputGetter.WIDTH_DICT.keys()

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

        coord = InputGetter.translate_user_coords(user_input)
        return Field(coord)

    @staticmethod
    def translate_user_coords(coordinate):
        row, col = InputGetter.LENGTH_DICT[coordinate[0]], InputGetter.WIDTH_DICT[coordinate[1]]
        return row, col

    @staticmethod
    def create_coords_translation_dictionary():
        length, width = 10, 10
        letters = string.ascii_uppercase
        rows_dictionary = dict()
        columns_dictionary = dict()

        for length_number in range(length):
            rows_dictionary[letters[length_number]] = length_number

        for width_number in range(width):
            columns_dictionary[str(width_number + 1)] = width_number
        return rows_dictionary, columns_dictionary

    @staticmethod
    def get_AI_shot_coord(pl_object):
        ROW_IDX = 0
        COL_IDX = 1
        hits = pl_object.get_hits()
        misses = pl_object.get_misses()
        if not hits:
            return random.choice(pl_object.opp_copy_bd.get_fields_by_type())
        elif len(hits) == 1:
            potential_shots = list(set(InputGetter.get_neighs_of_shot(hits[0], pl_object)) - set(hits + misses))
            clear_shots = []

            for shot in potential_shots:
                if SUNK not in InputGetter.get_neighs_of_shot(shot, pl_object) and shot not in misses + hits:
                    clear_shots.append(shot)

            return random.choice(clear_shots)

        elif len(hits) >= 2:

            orientation = ROW_IDX if hits[0][ROW_IDX] == hits[1][ROW_IDX] else COL_IDX
            potential_shots = []

            for hit in hits:
                neighs = list(set(InputGetter.get_neighs_of_shot(hit, pl_object)) - set(hits + misses))
                for neigh in neighs:
                    if orientation == ROW_IDX and neigh[ROW_IDX] == hit[ROW_IDX] or\
                     orientation == COL_IDX and neigh[COL_IDX] == hit[COL_IDX]:
                        potential_shots.append(neigh)

            return random.choice(potential_shots)

    @staticmethod
    def get_neighs_of_shot(hit, pl_obj):
        ROW_INDEX = 0
        COL_INDEX = 1

        max_length = len(pl_obj.opp_copy_bd.fields)
        max_width = len(pl_obj.opp_copy_bd.fields[ROW_INDEX])
        """Get neighbour coords for given hit coords. Help function for AI shooting."""
        if hit[ROW_INDEX]+1 < max_length:
            upper = (hit[ROW_INDEX] + 1, hit[COL_INDEX])

            try:
                if pl_obj.shots_stats[upper] == SUNK:
                    upper = SUNK
            except KeyError:
                pass
        else:
            upper = None

        if hit[COL_INDEX]+1 < max_width:
            right = (hit[ROW_INDEX], hit[COL_INDEX] + 1)

            try:
                if pl_obj.shots_stats[right] == SUNK:
                    right = SUNK
            except KeyError:
                pass
        else:
            right = None

        if hit[ROW_INDEX]-1 >= 0:
            lower = (hit[ROW_INDEX] - 1, hit[COL_INDEX])

            try:
                if pl_obj.shots_stats[lower] == SUNK:
                    lower = SUNK
            except KeyError:
                pass
        else:
            lower = None

        if hit[COL_INDEX]-1 >= 0:
            left = (hit[ROW_INDEX], hit[COL_INDEX] - 1)

            try:
                if pl_obj.shots_stats[left] == SUNK:
                    left = SUNK
            except KeyError:
                pass
        else:
            left = None


        return [coord for coord in [lower, right, upper, left] if coord is not None]