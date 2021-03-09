class Field:
    def __init__(self, coord1, state=None):
        self.x = coord1[0]
        self.y = coord1[1]
        self.state = state

    def __repr__(self):
        return self.state

    def __str__(self):
        return self.state

    def set_state(self, state):
        self.state = state

