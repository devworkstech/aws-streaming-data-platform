terraform {
  required_version = ">= 1.5.0"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
}
provider "aws" { region = var.aws_region }
variable "aws_region" { type = string; default = "us-east-1" }
variable "project_name" { type = string; default = "fintech-streaming-platform" }

resource "aws_kinesis_stream" "events" {
  name             = "${var.project_name}-events"
  shard_count      = 1
  retention_period = 24
  encryption_type  = "KMS"
  kms_key_id       = "alias/aws/kinesis"
  stream_mode_details { stream_mode = "PROVISIONED" }
}

resource "aws_s3_bucket" "archive" { bucket_prefix = "${var.project_name}-archive-" }
resource "aws_s3_bucket_public_access_block" "archive" {
  bucket = aws_s3_bucket.archive.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}
resource "aws_s3_bucket_server_side_encryption_configuration" "archive" {
  bucket = aws_s3_bucket.archive.id
  rule { apply_server_side_encryption_by_default { sse_algorithm = "AES256" } }
}

output "stream_name" { value = aws_kinesis_stream.events.name }
output "archive_bucket" { value = aws_s3_bucket.archive.id }
