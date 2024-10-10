resource "aws_cloudwatch_event_rule" "weekday_working_hours" {
  name        = "weekday-working-hours"
  description = "Trigger Lambda function during weekday working hours (Mon-Fri 9 AM - 5 PM)"

  schedule_expression = "cron(0 9-17 ? * 2-6 *)"  # Every hour from 9 AM to 5 PM (UTC) Monday to Friday
}

# Target for the EventBridge Rule
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.weekday_working_hours.name
  target_id = "myLambdaFunction"
  arn       = aws_lambda_function.event_finder.arn

  depends_on = [aws_cloudwatch_event_rule.weekday_working_hours]
}