
class Ships:
    def __init__(self):
        self.fleet = []

    def add_ship(self, ship):
        self.fleet.append(ship)

    def get_ship_by_part(self, coord):

        for ship in self.fleet:
            if coord in ship.parts.keys():
                return ship
