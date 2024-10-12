resource "aws_dynamodb_table" "user_table" {
  name     = "Users"
  billing_mode   = "PROVISIONED"
  read_capacity = 5
  write_capacity = 5
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