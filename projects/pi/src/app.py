import tkinter as tk
from pi_estimator import PiEstimator
from gui import GUI

class App:
    def __init__(self):
        """Initialize the application with instances of PiEstimator and GUI."""
        self.pi_estimator = PiEstimator()
        self.gui = GUI()

    def run(self):
        """Start the GUI event loop."""
        self.gui.start()

if __name__ == '__main__':
    app = App()
    app.run()
