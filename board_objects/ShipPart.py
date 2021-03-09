from board_objects.Field import Field
from board_objects.consts import SHIP

class ShipPart(Field):
    def __init__(self, coord):
        super().__init__(coord)
        self.state = SHIP

    def __repr__(self):
        return f"ShipPart({self.x}, {self.y})"

    def __str__(self):
        return super().__str__()