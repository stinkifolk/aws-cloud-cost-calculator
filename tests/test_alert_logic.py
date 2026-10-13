
import unittest

from src.alert_logic import evaluate_spending


class TestSpendingAlerts(unittest.TestCase):
    def test_below_threshold(self):
        result = evaluate_spending(25, 100)

        self.assertFalse(result["alert"])

    def test_at_threshold(self):
        result = evaluate_spending(100, 100)

        self.assertTrue(result["alert"])

    def test_above_threshold(self):
        result = evaluate_spending(125, 100)

        self.assertTrue(result["alert"])

    def test_rejects_negative_amount(self):
        with self.assertRaises(ValueError):
            evaluate_spending(-1, 100)

    def test_rejects_zero_threshold(self):
        with self.assertRaises(ValueError):
            evaluate_spending(10, 0)


if __name__ == "__main__":
    unittest.main()
