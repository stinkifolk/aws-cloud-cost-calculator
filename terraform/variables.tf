
variable "aws_region" {
  description = "AWS region for the infrastructure"
  type        = string
  default     = "ap-southeast-1"
}

variable "project_name" {
  description = "Name used for AWS resources"
  type        = string
  default     = "cloud-cost-calculator"
}

variable "cost_threshold_usd" {
  description = "Provisional monthly spending alert threshold in USD"
  type        = number
  default     = 50

  validation {
    condition     = var.cost_threshold_usd > 0
    error_message = "The cost threshold must be greater than zero."
  }
}

variable "alert_email" {
  description = "Email address that will receive cost alerts"
  type        = string
}

variable "lambda_zip_path" {
  description = "Path to the packaged Lambda ZIP file"
  type        = string
  default     = "../build/lambda.zip"
}
