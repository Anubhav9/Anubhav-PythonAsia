resource "aws_vpc" "python_asia_vpc" {
  cidr_block = var.vpc_cidr_block
  tags = {
    Name = "${var.python_asia_nomenclature}-vpc"

  }
  
}