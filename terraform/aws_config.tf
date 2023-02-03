# Configure TF and AWS provider
terraform {
  required_version = ">= 1.2.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
}

# Configure AWS provider
provider "aws" {
  region = var.aws_region
}

resource "random_string" "random_suffix" {
  length  = 5
  special = false
  upper   = false
  keepers = {
    instance_ip = var.s3_bucket
  }
}

# Create a VPC
# resource "aws_vpc" "boston-rentsmart-etl-vpc" {
#   cidr_block = "10.0.0.0/16"
# }