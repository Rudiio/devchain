class Segment:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def set_position(self, x, y):
        self._x = x
        self._y = y

    def get_position(self):
        return (self._x, self._y)
