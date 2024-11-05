import math
import pytest
from src.pi_estimator import PiEstimator

# Constants for the test
KNOWN_PI = math.pi

# Test class for PiEstimator
class TestPiEstimator:
    # Test to check if the PiEstimator estimates Pi with the correct precision
    def test_estimate_pi_precision(self):
        # Initialize the PiEstimator
        pi_estimator = PiEstimator()

        # Define the precision we want to test and the tolerance for the comparison
        precision = 5  # This means we want to test up to 5 decimal places
        tolerance = 10 ** (-precision)

        # Estimate Pi using the PiEstimator
        estimated_pi = pi_estimator.estimate_pi(precision)

        # Check if the estimated value is close to the known value of Pi
        assert math.isclose(estimated_pi, KNOWN_PI, rel_tol=tolerance), (
            f"Estimated Pi is not within the tolerance of {tolerance} for the precision of {precision} decimal places."
        )

# This is a placeholder for additional tests that might be added in the future
# def test_other_features():
#     pass

# Run the tests if this file is executed directly
if __name__ == "__main__":
    pytest.main()
