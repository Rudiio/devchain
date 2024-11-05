import unittest
from unittest.mock import MagicMock
from src.gui import GUI
from src.pi_estimator import PiEstimator

class TestApplicationBehavior(unittest.TestCase):

    def test_gui_calculate_button_interaction(self):
        # Create a GUI instance with a mocked PiEstimator
        gui = GUI()
        gui.pi_estimator = MagicMock(spec=PiEstimator)
        gui.precision_input = MagicMock()
        gui.precision_input.get.return_value = '10'  # Mock user input for precision

        # Simulate the calculate button click
        gui.on_calculate_clicked()

        # Check if estimate_pi was called with the correct precision argument
        gui.pi_estimator.estimate_pi.assert_called_with(10)

if __name__ == '__main__':
    unittest.main()
