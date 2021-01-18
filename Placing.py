from time import sleep
from Shooting import clear_console
from Game_server import SHIP_SYMBOL, EMPTY_SYMBOL
class Placing:
    def __init__(self, coord1, coord2):
        self.coord1 = coord1
        self.coord2 = coord2

    
    def get_neighbours(self, board, ship_length):
        coordinates = (self.coord1, self.coord2)
        
        upper_row = get_upper_row(board, coordinates, ship_length)
        lower_row = get_lower_row(board, coordinates, ship_length)
        left_column = get_left_column(board, coordinates, ship_length)
        right_column = get_right_column(board, coordinates, ship_length)

        return upper_row + lower_row + left_column + right_column


    def is_correct(self, board_object, ship_length):
        row1, col1, row2, col2 = self.coord1[0], self.coord1[1], self.coord2[0], self.coord2[1]
        min_row, min_col = min(row1,row2), min(col1,col2)
        max_row, max_col = max(row1,row2), max(col1,col2)
        players_board = board_object.fields
        move_is_in_row = row1 == row2
        move_is_in_col = col1 == col2
        is_ship_out_of_board = lambda orientation, cd1, cd2: min(cd1,cd2) + ship_length > len(orientation)
    

        if not move_is_in_row and not move_is_in_col:
            return False

        if move_is_in_row:
            taken_areas_states = [state for state in players_board[row1][min_col:max_col+1]]
            if is_ship_out_of_board(players_board[0], col1, col2):
                return False
        else:
            taken_areas_states = [players_board[row_number][col1] for row_number in range(min_row, max_row+1)]
            if is_ship_out_of_board(players_board, row1, row2):
                return False

        neighbour_fields = self.get_neighbours(players_board, ship_length)
        is_ship_in_neighbour = SHIP_SYMBOL in neighbour_fields
        
        if is_ship_in_neighbour:
            return False

        return True if taken_areas_states.count(EMPTY_SYMBOL) == len(taken_areas_states) else False


    def place_single_ship(self, board_object, ship_length, player_ships):
        """Marking correct fields on board as ship."""
        row1, col1 = self.coord1[0], self.coord1[1]
        row2, col2 = self.coord2[0], self.coord2[1]
        ship_placing_counter = 0
        players_board = board_object.fields

        row_counter = min(row1, row2)
        col_counter = min(col1, col2)
        
        ship_coordinates_dict = {}
        
        while ship_placing_counter < ship_length:
            
            if col1 == col2:
                players_board[row_counter][col1] = SHIP_SYMBOL
                ship_coordinates_dict[(row_counter, col1)] = SHIP_SYMBOL
                row_counter += 1
            else:
                players_board[row1][col_counter] = SHIP_SYMBOL
                ship_coordinates_dict[(row1, col_counter)] = SHIP_SYMBOL
                col_counter += 1
                
            ship_placing_counter +=1

        player_ships.append(ship_coordinates_dict)


def get_upper_row(board, coords, ship_length):
    """Upper part of get_neighbour_fields"""
    row1, col1 = coords[0][0], coords[0][1]
    row2, col2 = coords[1][0], coords[1][1]
    min_col = min(col1,col2)
    if max(row1,row2) == len(board)-1:
        return []
    elif col1 == col2:
        return [board[max(row1,row2)+1][col1]] 
    else:
        return board[max(row1,row2)+1][min_col:min_col+ship_length]


def get_lower_row(board, coords, ship_length):
    """Lower part of get_neighbour_fields"""
    row1, col1 = coords[0][0], coords[0][1]
    row2, col2 = coords[1][0], coords[1][1]
    min_col = min(col1,col2)

    if min(row1,row2) == 0:
        return []
    elif col1 == col2:
        return [board[min(row1,row2)-1][col1]] 
    else:
        return board[min(row1,row2)-1][min_col:min_col+ship_length]


def get_left_column(board, coords, ship_length):
    """Left part of get_neighbour_fields"""
    row1, col1 = coords[0][0], coords[0][1]
    row2, col2 = coords[1][0], coords[1][1]
    min_row = min(row1,row2)
    if min(col1,col2) == 0:
        return []
    elif row1 == row2:
        return [board[row1][min(col1,col2)-1]] 
    else:
        return [board[min_row + counter][min(col1,col2)-1] for counter in range(0,ship_length)]


def get_right_column(board, coords, ship_length):
    """Right part of get_neighbour_fields"""
    row1, col1 = coords[0][0], coords[0][1]
    row2, col2 = coords[1][0], coords[1][1]
    min_row = min(row1,row2)
    if max(col1,col2) == len(board[0]) - 1:
        return []
    elif row1 == row2:
        return [board[row1][max(col1,col2)+1]] 
    else:
        return [board[min_row + counter][max(col1,col2)+1] for counter in range(0,ship_length)]


def service_placing(player_object, ships_lengths_list):   
    human_player = player_object.is_human_player
    
    for ship_length in ships_lengths_list:
        print(f"{player_object.nickname} placing turn")
        player_object.p_board.print()
        print(f"Placing ship with length: {ship_length}.")
        
        is_placing_invalid = True
        while is_placing_invalid:
            if human_player:
                coord1 = player_object.get_user_valid_coord()
                coord2 = player_object.get_user_valid_coord()
            else:
                coord1, coord2 = player_object.get_AI_valid_coords(ship_length)
                sleep(0.5)

            placing = Placing(coord1, coord2)
            is_placing_invalid = not placing.is_correct(player_object.p_board, ship_length)

        placing.place_single_ship(player_object.p_board, ship_length, player_object.ships_list)
        clear_console()
    
    print(f"{player_object.nickname} placing turn finished")
    player_object.p_board.print()
    input("Press enter to continue")
    clear_console()