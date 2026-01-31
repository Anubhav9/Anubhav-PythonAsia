resource "aws_eks_node_group" "python_asia_private_nodegroup" {
  cluster_name    = aws_eks_cluster.python_asia_eks_cluster.name
  node_group_name = "${var.python_asia_nomenclature}-private-nodegroup"
  node_role_arn   = aws_iam_role.node.arn
  subnet_ids      = [aws_subnet.python_asia_private_subnet.id]

  scaling_config {
    desired_size = 1
    min_size     = 1
    max_size     = 1
  }

  instance_types = ["t3.medium"]
  capacity_type  = "ON_DEMAND"

  depends_on = [
    aws_iam_role_policy_attachment.node_AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.node_AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.node_AmazonEC2ContainerRegistryReadOnly
  ]
}

resource "aws_eks_node_group" "python_asia_public_nodegroup" {
  cluster_name    = aws_eks_cluster.python_asia_eks_cluster.name
  node_group_name = "${var.python_asia_nomenclature}-public-nodegroup"
  node_role_arn   = aws_iam_role.node.arn
  subnet_ids      = [aws_subnet.python_asia_public_subnet.id]

  scaling_config {
    desired_size = 1
    min_size     = 1
    max_size     = 1
  }

  instance_types = ["t3.medium"]
  capacity_type  = "ON_DEMAND"

  depends_on = [
    aws_iam_role_policy_attachment.node_AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.node_AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.node_AmazonEC2ContainerRegistryReadOnly
  ]
}