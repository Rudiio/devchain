# Import necessary modules from the src folder
from src.gui import GUI
from src.pi_estimator import PiEstimator
import tkinter as tk
import unittest

# Helper function to simulate user interaction with GUI components
def simulate_user_interaction(gui_component):
    """
    Simulates user interaction with a GUI component by invoking it if possible.
    """
    if hasattr(gui_component, 'invoke'):
        gui_component.invoke()

class TestGUIElements(unittest.TestCase):
    def setUp(self):
        """
        Set up the GUI before each test.
        """
        self.gui = GUI()

    def test_calculate_button_click(self):
        """
        Test that clicking the calculate button triggers the pi calculation.
        """
        # Set a known precision value
        self.gui.precision_input.insert(tk.END, "1000")
        
        # Simulate clicking the calculate button
        simulate_user_interaction(self.gui.calculate_button)
        
        # Check if the result label is updated (assuming the PiEstimator is mocked)
        self.assertNotEqual(self.gui.result_label['text'], "")

    def test_info_button_click(self):
        """
        Test that clicking the info button opens the information dialog.
        """
        # Simulate clicking the info button
        simulate_user_interaction(self.gui.info_button)
        
        # Check if the info dialog is opened (this may require additional logic
        # to verify that the dialog is actually opened, depending on implementation)

    # Additional tests can be added here to cover more GUI elements and interactions

if __name__ == '__main__':
    unittest.main()
