resource "aws_s3_bucket" "python_asia_bucket" {
  bucket = "approval-letters-${var.python_asia_nomenclature}"
  tags = {
    Name = "approval-letters-${var.python_asia_nomenclature}"
  }
}

resource "aws_s3_bucket_public_access_block" "python_asia_bucket_public_access_block" {
  bucket = aws_s3_bucket.python_asia_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

