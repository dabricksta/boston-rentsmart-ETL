/* 
Done:
1. AWS Provider
2. S3 - folder
3. Lambda - IAM role, extract_data and clean_data functions, Cloudwatch event cron schedule and link to S3 bucket
4. Redshift - cluster, security group, read access to S3 

TODOs:
1. VPC and integrate with other reseources
2. S3 raw/cleaned folders(?)
3. Access to Lambda functions for cloudwatch events?
4. Lambda execution role?
*/

# Configure TF and AWS provider
terraform {
  required_version = ">= 1.2.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
      region = var.aws_region
    }
  }
}

# Configure AWS provider
# provider "aws" {
#   region = var.aws_region
# }

# Create a VPC
# resource "aws_vpc" "example" {
#   cidr_block = "10.0.0.0/16"
# }
# https://registry.terraform.io/providers/hashicorp/aws/latest/docs

########################################################################
##############################   S3   ##################################
########################################################################

# Create AWS S3 bucket
resource "aws_s3_bucket" "boston_rentsmart_ETL" {
  bucket = var.s3_bucket
  force_destroy = true # will delete contents of bucket when we run terraform destroy
}

# Create S3 bucket with subfolder for raw data (initial extraction)
resource "aws_s3_bucket_object" "raw" {
  bucket       = "${aws_s3_bucket.boston_rentsmart_ETL.id}"
  key          = "${var.s3_bucket}/raw/"
  content_type = "application/x-directory"
  force_destroy = true # will delete contents of bucket when we run terraform destroy
}

# Create subfolder for cleaned data
resource "aws_s3_bucket_object" "cleaned" {
  bucket       = "${aws_s3_bucket.boston_rentsmart_ETL.id}"
  key          = "${var.s3_bucket}/cleaned/"
  content_type = "application/x-directory"
  force_destroy = true # will delete contents of bucket when we run terraform destroy
}

########################################################################
############################## Lambda ##################################
########################################################################

# Create the first Lambda function that will extract the data from the API
resource "aws_lambda_function" "extract_data" {
  filename         = "https://github.com/dabricksta/boston-rentsmart-ETL/blob/main/extract_data.py"
  function_name    = "extract_data"
  role             = "${aws_iam_role.lambda_execution_role.arn}"
  handler          = "index.handler"
  runtime          = "python3.8"
  s3_bucket        = "${aws_s3_bucket_object.raw.bucket}"
  s3_key           = "extract_data.zip"
}

# Create the second Lambda function that will clean the data
resource "aws_lambda_function" "clean_data" {
  filename         = "https://github.com/dabricksta/boston-rentsmart-ETL/blob/main/clean_data.py"
  function_name    = "clean_data"
  role             = "${aws_iam_role.lambda_execution_role.arn}"
  handler          = "index.handler"
  runtime          = "python3.8"
  s3_bucket        = "${aws_s3_bucket_object.cleaned.bucket}"
}

# Schedule for extraction: 11pm every night
resource "aws_cloudwatch_event_rule" "extract_data_schedule" {
  name                = "extract_data_schedule"
  schedule_expression = "cron(0 11 * * ? *)"
}

# Link extract_data with the cloudwatch nightly schedule
resource "aws_cloudwatch_event_target" "extract_data_target" {
  rule = aws_cloudwatch_event_rule.extract_data_schedule.name
  arn  = aws_lambda_function.extract_data.arn
}

# Create S3 bucket event notification trigger for clean_data
resource "aws_s3_bucket_notification" "lambda_event" {
  bucket = "${var.s3_bucket}"
  lambda_function {
    lambda_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:my-lambda-function"
    events              = ["s3:ObjectCreated:*"]
  }
}

########################################################################
############################# Redshift #################################
########################################################################

# Configure redshift cluster. This will fall under free tier as of June 2022.
resource "aws_redshift_cluster" "redshift" {
  cluster_identifier     = "redshift-cluster-pipeline"
  skip_final_snapshot    = true # must be set so we can destroy redshift with terraform destroy
  master_username        = "awsuser"
  master_password        = var.db_password
  node_type              = "dc2.large"
  cluster_type           = "single-node"
  publicly_accessible    = "true"
  iam_roles              = [aws_iam_role.redshift_role.arn]
  vpc_security_group_ids = [aws_security_group.sg_redshift.id]
}

# Configure security group for Redshift allowing all inbound/outbound traffic
resource "aws_security_group" "sg_redshift" {
  name = "sg_redshift"
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create S3 Read only access role. This is assigned to Redshift cluster so that it can read data from S3
resource "aws_iam_role" "redshift_role" {
  name                = "RedShiftLoadRole"
  managed_policy_arns = ["arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"]
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "redshift.amazonaws.com"
        }
      },
    ]
  })
}