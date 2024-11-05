from symbol import Symbol

class Player:
    def __init__(self, name, symbol):
        self._name = name
        self._symbol = symbol

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_symbol(self):
        return self._symbol
