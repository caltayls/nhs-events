resource "aws_lambda_function" "emailer" {
  function_name = "emailer"
  role          = aws_iam_role.emailer_role.arn
  runtime = "python3.12"
  architectures = ["x86_64"]
  handler = "src.lambda_handler.lambda_handler"
  image_uri = ""

#   filename = data.archive_file.emailer.output_path
#   source_code_hash = filebase64sha256(data.archive_file.emailer.output_path)

#   layers = [
#     aws_lambda_layer_version.module_layer.arn,
#     aws_lambda_layer_version.aws_utils.arn
#   ]
}

resource "aws_iam_role" "emailer_role" {
  name = "emailer-role"

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

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.emailer_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "email_lambda_policy" {
  name = "s3-policy"
  role = aws_iam_role.emailer_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject"
        ]
        Effect   = "Allow"
        Resource = "${aws_s3_bucket.nhs_events.arn}/*"
      },
      {
        Action = [
          "dynamodb:Scan",
          "dynamodb:query"
        ]
        Effect   = "Allow"
        Resource = aws_dynamodb_table.user_table.arn
      }
    ]
  })
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.emailer.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.nhs_events.arn
}

# data "archive_file" "emailer" {
#   type        = "zip"
#   source_dir = "${path.module}/../emailer"
#   output_path = "${path.module}/emailer.zip"
#   excludes = ["venv", "tests", "**/__pycache__"]
# }


