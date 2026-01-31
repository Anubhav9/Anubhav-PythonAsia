resource "aws_iam_policy" "python_asia_s3_bucket_iam_policy" {
  name        = "s3-bucket-iam-policy-${var.python_asia_nomenclature}"
  path        = "/"
  description = "S3 Bucket for Python Asia Bucket"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:ListBucket",
        ]
        Effect   = "Allow"
        Resource = aws_s3_bucket.python_asia_bucket.arn
      },
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Effect   = "Allow"
        Resource = "${aws_s3_bucket.python_asia_bucket.arn}/*"
      }
    ]
  })
  
}



# OIDC issuer URL from the cluster
locals {
  oidc_host_path  = replace(local.oidc_issuer_url, "https://", "")
}


resource "aws_iam_role" "pod_for_s3_rw" {
  name = "PodForS3ReadWrite-${var.python_asia_nomenclature}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = "sts:AssumeRoleWithWebIdentity",
        Principal = {
          Federated = aws_iam_openid_connect_provider.eks.arn
        },
        Condition = {
          StringEquals = {
            "${local.oidc_host_path}:sub" = "system:serviceaccount:default:sa-decision-service",
            "${local.oidc_host_path}:aud" = "sts.amazonaws.com"
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "python_asia_s3_bucket_role_policy_attachment" {
  role = aws_iam_role.pod_for_s3_rw.id
  policy_arn = aws_iam_policy.python_asia_s3_bucket_iam_policy.arn
  
}
