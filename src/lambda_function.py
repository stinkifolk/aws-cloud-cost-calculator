
import json
import os
from datetime import date, datetime, timezone

import boto3

from src.alert_logic import evaluate_spending
from src.cost_report import get_monthly_cost


def lambda_handler(event, context, ce_client=None, sns_client=None, today=None):
    if today is None:
        today = datetime.now(timezone.utc).date()

    # End date is exclusive, so this covers the current month
    # through yesterday. Today's costs may not be available yet.
    start_date = today.replace(day=1)
    end_date = today

    if start_date >= end_date:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "No completed days available for this month yet.",
                "notification_sent": False,
            }),
        }

    threshold = float(os.environ.get("COST_THRESHOLD_USD", "50"))
    topic_arn = os.environ.get("SNS_TOPIC_ARN")

    if ce_client is None:
        ce_client = boto3.client("ce", region_name="us-east-1")

    report = get_monthly_cost(
        start_date.isoformat(),
        end_date.isoformat(),
        ce_client=ce_client,
    )

    # Current-month billing data can be incomplete or estimated.
    report["data_status"] = "provisional"

    alert = evaluate_spending(
        report["amount"],
        threshold,
        report["unit"],
    )

    result = {
        "report": report,
        "alert": alert,
        "notification_sent": False,
    }

    if alert["alert"] and topic_arn and report["data_available"]:
        if sns_client is None:
            sns_client = boto3.client("sns")

        message = {
            **result,
            "notice": (
                "This is a provisional current-month cost report. "
                "Cost Explorer data may be delayed or estimated. "
                "Verify the amount in AWS Billing before acting."
            ),
        }

        sns_client.publish(
            TopicArn=topic_arn,
            Subject="AWS Cost Threshold Alert (Provisional)",
            Message=json.dumps(message, indent=2),
        )

        result["notification_sent"] = True

    return {
        "statusCode": 200,
        "body": json.dumps(result),
    }
