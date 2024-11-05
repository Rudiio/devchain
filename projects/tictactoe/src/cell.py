from symbol import Symbol

class Cell:
    def __init__(self):
        self._symbol = Symbol.EMPTY

    def is_empty(self):
        return self._symbol == Symbol.EMPTY

    def get_symbol(self):
        return self._symbol

    def set_symbol(self, symbol):
        if isinstance(symbol, Symbol):
            self._symbol = symbol
