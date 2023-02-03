# Create AWS S3 bucket
resource "aws_s3_bucket" "rentsmart_bucket" {
  bucket        = "${var.s3_bucket}-${random_string.random_suffix.result}"
  force_destroy = true # will delete contents of bucket when we run terraform destroy
}

# Set access control of bucket to private
resource "aws_s3_bucket_acl" "s3_rentsmart_bucket_acl" {
  bucket = aws_s3_bucket.rentsmart_bucket.id
  acl    = "private"
}

# Create S3 bucket with subfolder for raw data (initial extraction)
resource "aws_s3_object" "raw" {
  bucket        = aws_s3_bucket.rentsmart_bucket.id
  key           = "/raw/"
  content_type  = "application/x-directory"
  force_destroy = true # will delete contents of bucket when we run terraform destroy
}

# Create subfolder for cleaned data
resource "aws_s3_object" "cleaned" {
  bucket        = aws_s3_bucket.rentsmart_bucket.id
  key           = "/cleaned/"
  content_type  = "application/x-directory"
  force_destroy = true # will delete contents of bucket when we run terraform destroy
}