# data archive_file "lambda_modules" {
#   type = "zip"
#   source_dir = "${path.module}/../lambda_modules_layer"
#   output_path = "${path.module}/lambda_modules_layer.zip"
#   excludes = ["**/__pychache__", "**/bin", "**/*.dist-info"]
#
# }
#
# resource "aws_lambda_layer_version" "module_layer" {
#   layer_name = "module-layer"
#   compatible_runtimes = ["python3.12"]
#   filename = data.archive_file.lambda_modules.output_path
#   source_code_hash    = filebase64sha256(data.archive_file.lambda_modules.output_path)
#
#   compatible_architectures = ["x86_64"]
#
# }