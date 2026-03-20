resource "aws_s3_bucket" "python_asia_bucket" {
  bucket = var.object_store_bucket_name
  tags = {
    Name = var.object_store_bucket_name
  }
}

resource "aws_s3_bucket_public_access_block" "python_asia_bucket_public_access_block" {
  bucket = aws_s3_bucket.python_asia_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

