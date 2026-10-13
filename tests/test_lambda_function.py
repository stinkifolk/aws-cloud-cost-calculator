
import json
import os
import unittest
from datetime import date
from unittest.mock import Mock, patch

from src.lambda_function import lambda_handler


class TestLambdaHandler(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_returns_report_without_sending_notification(self):
        ce_client = Mock()
        ce_client.get_cost_and_usage.return_value = {
            "ResultsByTime": [
                {
                    "Total": {
                        "UnblendedCost": {
                            "Amount": "10.00",
                            "Unit": "USD",
                        }
                    },
                    "Estimated": True,
                }
            ]
        }

        sns_client = Mock()

        response = lambda_handler(
            {},
            None,
            ce_client=ce_client,
            sns_client=sns_client,
            today=date(2026, 10, 13),
        )

        body = json.loads(response["body"])

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(body["report"]["amount"], 10.0)
        self.assertEqual(body["report"]["data_status"], "provisional")
        self.assertFalse(body["notification_sent"])
        sns_client.publish.assert_not_called()

    @patch.dict(
        os.environ,
        {
            "COST_THRESHOLD_USD": "50",
            "SNS_TOPIC_ARN": "arn:aws:sns:ap-southeast-1:123456789012:test",
        },
    )
    def test_sends_alert_when_threshold_reached(self):
        ce_client = Mock()
        ce_client.get_cost_and_usage.return_value = {
            "ResultsByTime": [
                {
                    "Total": {
                        "UnblendedCost": {
                            "Amount": "75.00",
                            "Unit": "USD",
                        }
                    },
                    "Estimated": True,
                }
            ]
        }

        sns_client = Mock()

        response = lambda_handler(
            {},
            None,
            ce_client=ce_client,
            sns_client=sns_client,
            today=date(2026, 10, 13),
        )

        body = json.loads(response["body"])

        self.assertTrue(body["alert"]["alert"])
        self.assertTrue(body["notification_sent"])
        sns_client.publish.assert_called_once()

    def test_skips_reporting_on_first_day_of_month(self):
        ce_client = Mock()

        response = lambda_handler(
            {},
            None,
            ce_client=ce_client,
            today=date(2026, 10, 1),
        )

        body = json.loads(response["body"])

        self.assertEqual(response["statusCode"], 200)
        self.assertFalse(body["notification_sent"])
        ce_client.get_cost_and_usage.assert_not_called()


if __name__ == "__main__":
    unittest.main()
