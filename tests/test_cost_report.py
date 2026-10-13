
import unittest
from unittest.mock import Mock

from src.cost_report import get_monthly_cost


class TestMonthlyCost(unittest.TestCase):
    def test_returns_monthly_cost(self):
        client = Mock()
        client.get_cost_and_usage.return_value = {
            "ResultsByTime": [
                {
                    "Total": {
                        "UnblendedCost": {
                            "Amount": "12.50",
                            "Unit": "USD",
                        }
                    },
                    "Estimated": False,
                }
            ]
        }

        result = get_monthly_cost(
            "2026-09-01",
            "2026-10-01",
            ce_client=client,
        )

        self.assertEqual(result["amount"], 12.5)
        self.assertEqual(result["unit"], "USD")
        self.assertFalse(result["estimated"])

    def test_rejects_invalid_date_range(self):
        with self.assertRaises(ValueError):
            get_monthly_cost("2026-10-01", "2026-09-01")

    def test_handles_empty_results(self):
        client = Mock()
        client.get_cost_and_usage.return_value = {
            "ResultsByTime": []
        }

        result = get_monthly_cost(
            "2026-09-01",
            "2026-10-01",
            ce_client=client,
        )

        self.assertEqual(result["amount"], 0.0)


if __name__ == "__main__":
    unittest.main()
