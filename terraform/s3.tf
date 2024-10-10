resource "aws_s3_bucket" "nhs_events" {
  bucket = "nhs-events"
}

resource "aws_s3_bucket_notification" "nhs_events_notification" {
  bucket = aws_s3_bucket.nhs_events.bucket

  lambda_function {
    lambda_function_arn = aws_lambda_function.event_finder.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "AWSLogs/"
    filter_suffix       = ".log"
  }

  depends_on = [aws_lambda_permission.allow_bucket]
}