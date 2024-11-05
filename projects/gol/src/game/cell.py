class Cell:
    def __init__(self, is_alive: bool):
        self._is_alive = is_alive

    @property
    def is_alive(self) -> bool:
        return self._is_alive

    @is_alive.setter
    def is_alive(self, is_alive: bool):
        self._is_alive = is_alive

    def set_is_alive(self, is_alive: bool):
        self._is_alive = is_alive

    def toggle_state(self):
        self._is_alive = not self._is_alive
