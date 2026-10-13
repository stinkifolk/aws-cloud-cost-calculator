
output "lambda_function_name" {
  description = "Deployed cost-report Lambda function"
  value       = aws_lambda_function.cost_report.function_name
}

output "sns_topic_arn" {
  description = "SNS topic for cost alerts"
  value       = aws_sns_topic.cost_alerts.arn
}

output "aws_region" {
  description = "Deployment region"
  value       = var.aws_region
}
