# OIDC issuer URL from the cluster
locals {
  oidc_issuer_url = aws_eks_cluster.python_asia_eks_cluster.identity[0].oidc[0].issuer
}

# Fetch the TLS cert fingerprint for the issuer (needed by IAM)
data "tls_certificate" "eks_oidc" {
  url = local.oidc_issuer_url
}

# Create the IAM OIDC provider in your AWS account
resource "aws_iam_openid_connect_provider" "eks" {
  url             = local.oidc_issuer_url
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.eks_oidc.certificates[0].sha1_fingerprint]
}
