resource "aws_dynamodb_table" "user_table" {
  name     = "user-table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key = "freq"
  range_key = "uuid"

  attribute {
    name = "freq"
    type = "S"
  }
  attribute {
    name = "uuid"
    type = "S"
  }
}