# AWS Cloud Cost Calculator

A serverless Python project that retrieves AWS cost data, evaluates monthly spending against a configurable threshold, and sends email alerts through Amazon SNS.

## Table of Contents

- [Project Status](#project-status)
- [Architecture](#architecture)
- [Technology](#technology)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Run Tests Locally](#run-tests-locally)
- [Configuration](#configuration)
- [Cost and Safety](#cost-and-safety)
- [Security](#security)
- [License](#license)

## Project Status

| Area | Status |
| --- | --- |
| Python unit tests | 11 passing |
| Terraform configuration | Validated locally |
| Lambda deployment package | Built and locally verified |
| AWS infrastructure | **Not confirmed deployed. Do not assume resources exist.** |
| Billing data | Current-month figures may be delayed or estimated |

## Architecture

1. **Amazon EventBridge** triggers the Lambda function daily.
2. **AWS Lambda** retrieves cost data from AWS Cost Explorer.
3. The application compares reported spending with a configurable USD threshold.
4. **Amazon SNS** sends an email notification when the threshold is reached and cost data is available.
5. **Amazon CloudWatch Logs** stores execution logs, configured for 14-day retention.

## Technology

- Python 3.13
- AWS Lambda
- AWS Cost Explorer
- Amazon SNS
- Amazon EventBridge
- Amazon CloudWatch
- Terraform
- Python `unittest`

## Repository Structure

```text
.
├── src/
│   ├── alert_logic.py
│   ├── cost_report.py
│   └── lambda_function.py
├── tests/
│   ├── test_alert_logic.py
│   ├── test_cost_report.py
│   └── test_lambda_function.py
├── terraform/
│   ├── main.tf
│   ├── outputs.tf
│   ├── variables.tf
│   ├── terraform.tfvars.example
│   └── .terraform.lock.hcl
└── .gitignore
```

The Lambda deployment ZIP is generated under `build/` and is excluded from Git.

## Prerequisites

- Python 3.13
- Terraform 1.5 or later
- AWS CLI, if deploying to AWS
- An AWS account with the necessary permissions
- Cost Explorer enabled for the account
- An email address for alert notifications

## Run Tests Locally

From the repository root:

```cmd
py -3.13 -m unittest discover -s tests -v
```

Validate the Terraform configuration:

```cmd
terraform -chdir=terraform fmt -check
terraform -chdir=terraform validate
```

> These local tests and validation commands do not deploy AWS infrastructure.

## Configuration

Create your private variables file from the example:

```cmd
copy terraform\terraform.tfvars.example terraform\terraform.tfvars
```

Edit `terraform\terraform.tfvars` and set the alert email address. The actual `terraform.tfvars` file is excluded from Git.

The default monthly alert threshold is **USD 50**. Change it to a suitable value for your own account.

## Cost and Safety

> **This project is not a spending cap and does not guarantee a zero-dollar AWS bill.**

- Terraform deployment creates AWS resources that may incur charges.
- Cost Explorer API usage, Lambda executions, EventBridge, SNS notifications, and CloudWatch Logs may have pricing implications depending on usage and account eligibility.
- Cost Explorer data can be delayed or estimated.
- Email alerts are notifications, not automatic shutdowns.
- Review AWS Billing and Free Tier eligibility before deploying.
- Keep the infrastructure undeployed if your goal is to avoid project-related AWS resource charges.

Before deploying, review the Terraform configuration and run `terraform plan` only when you are ready to make AWS API calls. Review the proposed changes and estimated costs carefully before considering an `apply`.

## Security

- The Lambda role is intended to use least-privilege permissions.
- The alert email and local Terraform variables file should not be committed.
- Review IAM policies and logging permissions before deployment.
- Never commit AWS access keys, secret keys, credentials, Terraform state files, or saved plan files.

## License

No license has been specified yet. All rights remain with the repository owner unless a license is added.
