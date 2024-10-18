import unittest
from calculator import *

class TestCalculator(unittest.TestCase):
    """
    This class contains unit tests for the Calculator class.
    """

    def test_add(self):
        """
        Test the add method of the Calculator class.

        This test verifies if the add method correctly adds two numbers.

        Parameters:
        None

        Returns:
        None
        """
        # Create an instance of the Calculator class
        calculator = Calculator()

        # Call the add method with two numbers and store the result
        result = calculator.add(2, 5)

        # Use the assertEqual method to verify if the result is equal to the expected value
        # If the result is not equal to the expected value, the test will fail
        self.assertEqual(result, 7)         # assertEqual verifies if the value is equal to the result of


if __name__ == '__main__':
    # Run the unit tests when the script is executed directly
    unittest.main()