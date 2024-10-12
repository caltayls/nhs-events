data "archive_file" "aws_utils_zip" {
  source_dir = "${path.module}/../aws_utils"
  output_path = "${path.module}/aws_utils.zip"
  type        = "zip"
}

resource "aws_lambda_layer_version" "aws_utils" {
  layer_name = "aws-utils"
  compatible_runtimes = ["python3.12"]
  filename = data.archive_file.aws_utils_zip.output_path
  source_code_hash    = filebase64sha256(data.archive_file.aws_utils_zip.output_path)
}