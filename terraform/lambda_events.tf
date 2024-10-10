data "archive_file" "event_finder" {
  type        = "zip"
  source_dir  = "${path.module}/../event_finder"
  output_path = "${path.module}/event_finder.zip"
  excludes = ["venv", "tests"]


}

resource "aws_lambda_function" "event_finder" {
  function_name = "event-finder"
  role          = aws_iam_role.event_finder_role.arn
  runtime = "python3.12"
  handler = "src.lambda_handler.lambda_handler"

  filename      = data.archive_file.event_finder.output_path
  source_code_hash = filebase64sha256(data.archive_file.event_finder.output_path)
}

resource "aws_iam_role" "event_finder_role" {
  name = "event-finder-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}


resource "aws_iam_role_policy_attachment" "event_lambda_basic_execution" {
  role       = aws_iam_role.event_finder_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "event_lambda_policies" {
  name = "event-lambda-policies"
  role = aws_iam_role.event_finder_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Effect   = "Allow"
        Resource = "${aws_s3_bucket.nhs_events.arn}/*"
      }
    ]
  })
}


resource "aws_lambda_permission" "allow_event_bridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.event_finder.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.weekday_working_hours.arn
}