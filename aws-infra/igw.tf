resource "aws_internet_gateway" "python_asia_internet_gateway" {
  vpc_id = aws_vpc.python_asia_vpc.id
  tags = {
    Name = "${var.python_asia_nomenclature}-internet-gateway"
  }
  
}