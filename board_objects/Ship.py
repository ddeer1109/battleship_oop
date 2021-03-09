from board_objects.consts import SHIP, SUNK


class Ship:
    def __init__(self, ships_parts_dicts):
        self.parts = ships_parts_dicts
        self.sunk = False

    def __repr__(self):
        return f"{len(self.parts)}{self.sunk}"[0:2]

    def get_part(self, coord):
        return self.parts[(coord[0], coord[1])]

    def not_sunk(self):
        return SHIP in [part.state for part in self.parts.values()]

    def update_sunk_state(self):
        if not self.not_sunk():
            for part_key in self.parts.keys():
                self.parts[part_key].set_state(SUNK)
            self.sunk = True
