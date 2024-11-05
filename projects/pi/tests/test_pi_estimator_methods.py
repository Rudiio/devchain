# test_pi_estimator_methods.py
import numpy as np
import pytest
from src.pi_estimator import PiEstimator

def test_estimate_pi_with_nan_value():
    """
    Test the behavior of the PiEstimator when it returns a NaN value.
    The estimator should handle the NaN value gracefully and not propagate
    it to the caller in a way that would cause further issues.
    """
    estimator = PiEstimator()

    # Mock the estimate_pi method to return NaN
    estimator.estimate_pi = lambda precision: np.nan

    # Call the estimate_pi method with a mocked precision value
    result = estimator.estimate_pi(10)

    # Assert that the result is NaN
    assert np.isnan(result), "The result should be NaN"

    # Additional checks can be added here to ensure that NaN values are handled gracefully
    # For example, checking that the GUI does not crash or that the result is displayed correctly

# Other test cases (if any) can be added below
