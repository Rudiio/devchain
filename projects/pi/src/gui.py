import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pi_estimator import PiEstimator
import numpy as np

class GUI:
    MAX_PRECISION = 15  # Class-level constant for maximum precision

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PiQuest: The Precision Frontier")
        self.pi_estimator = PiEstimator()
        self.init_components()

    def init_components(self):
        """Initialize all GUI components."""
        # Precision input
        tk.Label(self.root, text="Enter precision level:").pack()
        self.precision_input = tk.Entry(self.root)
        self.precision_input.pack()

        # Calculate button
        self.calculate_button = tk.Button(self.root, text="Calculate Pi", command=self.on_calculate_clicked)
        self.calculate_button.pack()

        # Result label
        self.result_label = tk.Label(self.root, text="Pi estimation will appear here.")
        self.result_label.pack()

        # Info button
        self.info_button = tk.Button(self.root, text="Info", command=self.show_info)
        self.info_button.pack()

        # Pi visualization (placeholder for matplotlib figure)
        self.pi_visualization = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.pi_visualization, master=self.root)
        self.canvas.get_tk_widget().pack()

    def start(self):
        """Run the main event loop of the tkinter GUI."""
        self.root.mainloop()

    def update_result(self, pi_estimate):
        """Display the estimated Pi value or an error if the estimate is invalid."""
        # Check if pi_estimate is an array and if any element is NaN
        if isinstance(pi_estimate, np.ndarray) and np.isnan(pi_estimate).any():
            self.result_label.config(text="Error: Invalid Pi estimation.")
            messagebox.showerror("Error", "Invalid Pi estimation. Please try again with different parameters.")
        else:
            self.result_label.config(text=f"Estimated Pi: {pi_estimate}")

    def show_info(self):
        """Display the method description."""
        method_description = self.pi_estimator.get_method_description()
        messagebox.showinfo("Pi Estimation Method", method_description)

    def on_calculate_clicked(self):
        """Handle the event when the calculate button is clicked."""
        try:
            precision = int(self.precision_input.get())
            if precision < 10:
                raise ValueError("Precision level must be at least 10.")
            if precision > GUI.MAX_PRECISION:
                raise ValueError(f"Precision level must not exceed {GUI.MAX_PRECISION}.")
            pi_estimate = self.pi_estimator.estimate_pi(precision)
            self.update_result(pi_estimate)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
