import numpy as np

class PiEstimator:
    def __init__(self):
        self.default_precision = 10  # Default precision
        self.current_precision = self.default_precision
        self.last_estimate = None

    def estimate_pi(self, precision):
        """
        Estimate the value of Pi to the specified precision using the
        Gauss-Legendre algorithm, which is known for its rapid convergence.
        The precision parameter specifies the number of decimal places desired,
        not the number of iterations. Adjust the number of iterations to ensure
        the desired precision is met.
        """
        # The precision is set directly by the user input
        self.current_precision = precision

        # Initialize variables for the Gauss-Legendre algorithm
        # Using higher precision data types to prevent underflow
        a = np.float64(1.0)
        b = np.float64(1 / np.sqrt(2))
        t = np.float64(1 / 4.0)
        p = np.float64(1.0)

        # Calculate the number of iterations needed to achieve the desired precision
        # Each iteration approximately doubles the number of correct digits
        # The number of iterations should be based on the desired number of decimal places
        iterations = int(np.ceil(np.log2(10**self.current_precision)))

        # Iteratively refine the estimate of Pi
        for _ in range(iterations):
            a_next = (a + b) / 2
            b = np.sqrt(a * b)
            t -= p * (a - a_next) ** 2
            a = a_next
            p *= 2

            # Check to prevent underflow and invalid operations immediately after 't' calculation
            if t < np.finfo(np.float64).tiny:
                # Instead of raising an error, we adjust 't' to the smallest positive number
                t = np.finfo(np.float64).tiny

            # Additional check for invalid operations
            if a == 0 or b == 0:
                raise ValueError("Invalid operation encountered in calculations.")

        # Calculate pi using the final a, b, and t values
        pi_estimate = (a + b) ** 2 / (4 * t)
        # Round the result to the desired precision
        self.last_estimate = np.round(pi_estimate, decimals=self.current_precision)
        return self.last_estimate

    def get_method_description(self):
        """
        Return a string describing the Gauss-Legendre algorithm used to estimate Pi.
        This method provides educational information about the algorithm to the user.
        """
        return ("The Gauss-Legendre algorithm is used to estimate Pi. "
                "It is an iterative algorithm that rapidly converges to Pi "
                "with a high degree of accuracy. This method is based on "
                "arithmetic-geometric mean calculations and efficiently "
                "produces multiple correct digits of Pi per iteration.")

    def reset(self):
        """
        Clear any stored values from previous calculations to ensure
        independent estimations. This method is called before starting a new
        Pi estimation process to avoid any interference from the last estimate.
        """
        self.last_estimate = None
        self.current_precision = self.default_precision  # Reset precision to default
