resource "aws_vpc" "vpc_python_asia_talk" {
  cidr_block = var.vpc_cidr_block
  instance_tenancy = "default"
  tags = {
    Name = "${var.python_asia_talk}-vpc"
  }
  
}