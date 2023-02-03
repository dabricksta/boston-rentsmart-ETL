
# Create the first Lambda function that will extract the data from the API
resource "aws_lambda_function" "extract_data" {
  filename         = "https://github.com/dabricksta/boston-rentsmart-ETL/blob/main/extract_data.py"
  function_name    = "extract_data"
  role             = "${aws_iam_role.lambda_execution_role.arn}"
  handler          = "index.handler"
  runtime          = "python3.8"
  s3_bucket        = "${aws_s3_object.raw.bucket}"
  s3_key           = "extract_data.zip"
}

# Resource policy for CloudWatch to trigger data exraction Lambda
resource "aws_lambda_permission" "allow_cloudwatch_to_invoke_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.extract_data.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.extract_data_schedule.arn
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

# Data cleaning
# Create the second Lambda function that will clean the data
resource "aws_lambda_function" "clean_data" {
  filename         = "https://github.com/dabricksta/boston-rentsmart-ETL/blob/main/clean_data.py"
  function_name    = "clean_data"
  role             = "${aws_iam_role.lambda_execution_role.arn}"
  handler          = "index.handler"
  runtime          = "python3.8"
  s3_bucket        = "${aws_s3_object.cleaned.bucket}"
}

# Create S3 bucket event notification trigger for clean_data
resource "aws_s3_bucket_notification" "lambda_event" {
  bucket = "${var.s3_bucket}"
  lambda_function {
    lambda_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:my-lambda-function"
    events              = ["s3:ObjectCreated:*"]
  }
}
