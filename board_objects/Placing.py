from time import sleep
# from Shooting import clear_console
# from consts import SHIP, EMPTY
from board_objects.Field import Field
from board_objects.consts import SHIP, EMPTY
from board_objects.ShipPart import ShipPart
from board_objects.Ship import Ship

class Placing:
    def __init__(self, coord1, coord2):
        self.cd1 = coord1
        self.cd2 = coord2

    def get_neighbours(self, board, ship_length):
        coordinates = (self.cd1, self.cd2)

        upper_row = Placing.get_upper_row(board, coordinates, ship_length)
        lower_row = Placing.get_lower_row(board, coordinates, ship_length)
        left_column = Placing.get_left_column(board, coordinates, ship_length)
        right_column = Placing.get_right_column(board, coordinates, ship_length)

        return upper_row + lower_row + left_column + right_column

    @staticmethod
    def get_upper_row(board, coords, ship_length):
        """Upper part of get_neighbour_fields"""
        row1, col1 = coords[0].x, coords[0].y
        row2, col2 = coords[1].x, coords[1].y
        min_col = min(col1, col2)
        try:
            if col1 == col2:
                return [board[max(row1, row2) + 1][col1]]
            else:
                return board[max(row1, row2) + 1][min_col:min_col + ship_length]
        except IndexError:
            return []

    @staticmethod
    def get_lower_row(board, coords, ship_length):
        """Lower part of get_neighbour_fields"""
        row1, col1 = coords[0].x, coords[0].y
        row2, col2 = coords[1].x, coords[1].y
        min_col = min(col1, col2)

        try:
            if col1 == col2:
                return [board[min(row1, row2) - 1][col1]]
            else:
                return board[min(row1, row2) - 1][min_col:min_col + ship_length]
        except IndexError:
            return []

    @staticmethod
    def get_left_column(board, coords, ship_length):
        """Left part of get_neighbour_fields"""
        row1, col1 = coords[0].x, coords[0].y
        row2, col2 = coords[1].x, coords[1].y
        min_row = min(row1, row2)

        try:
            if row1 == row2:
                return [board[row1][min(col1, col2) - 1]]
            else:
                return [board[min_row + counter][min(col1, col2) - 1] for counter in range(0, ship_length)]
        except IndexError:
            return []

    @staticmethod
    def get_right_column(board, coords, ship_length):
        """Right part of get_neighbour_fields"""
        row1, col1 = coords[0].x, coords[0].y
        row2, col2 = coords[1].x, coords[1].y
        min_row = min(row1, row2)

        try:
            if row1 == row2:
                return [board[row1][max(col1, col2) + 1]]
            else:
                return [board[min_row + counter][max(col1, col2) + 1] for counter in range(0, ship_length)]
        except IndexError:
            return []

    def is_correct(self, board_object, ship_length):
        row1, col1, row2, col2 = self.cd1.x, self.cd1.y, self.cd2.x, self.cd2.y
        min_row, min_col = min(row1, row2), min(col1, col2)
        players_board = board_object.fields
        move_is_in_row = row1 == row2
        move_is_in_col = col1 == col2
        is_ship_out_of_board = min_row < 0 or min_col < 0 \
                               or (move_is_in_col and min_row + ship_length > board_object.length) \
                               or (move_is_in_row and min_col + ship_length > board_object.width)

        if not move_is_in_row and not move_is_in_col or is_ship_out_of_board:
            return False

        if move_is_in_row:
            taken_areas_states = [field.state for field in players_board[row1][min_col:min_col + ship_length]]
        else:
            taken_areas_states = [
                players_board[row_number][col1].state for row_number in range(min_row, min_row+ship_length)]

        neighbour_fields = self.get_neighbours(players_board, ship_length)
        is_ship_in_neighbour = SHIP in [field.state for field in neighbour_fields]

        if is_ship_in_neighbour:
            return False

        return True if taken_areas_states.count(EMPTY) == len(taken_areas_states) else False

    def place_ship(self, board_object, ship_length, player_ships):
        """Marking correct fields on board as ship."""
        row1, col1 = self.cd1.x, self.cd1.y
        row2, col2 = self.cd2.x, self.cd2.y
        ship_placing_counter = 0

        row_counter = min(row1, row2)
        col_counter = min(col1, col2)

        ship_coordinates = {}

        while ship_placing_counter < ship_length:

            if col1 == col2:
                ship_part = ShipPart((row_counter, col1))
                row_counter += 1
            else:
                ship_part = ShipPart((row1, col_counter))
                col_counter += 1

            board_object.set_object_on_board(ship_part)
            ship_coordinates[(ship_part.x, ship_part.y)] = ship_part
            ship_placing_counter += 1

        player_ships.add_ship(Ship(ship_coordinates))
