resource "aws_route_table" "python_asia_talk_public_route_table" {
  vpc_id = aws_vpc.vpc_python_asia_talk.id
  route {
    cidr_block = var.python_asia_talk_public_route
    gateway_id = aws_internet_gateway.python_asia_talk_internet_gateway.id
  }

  tags = {
    Name = "${var.python_asia_talk}-public-route-table"
  }
  
}

resource "aws_route_table" "python_asia_talk_private_route_table" {
  vpc_id = aws_vpc.vpc_python_asia_talk.id
  route {
    cidr_block = var.python_asia_talk_public_route
    gateway_id = aws_nat_gateway.python_asia_talk_nat_gateway.id
  }
  tags = {
    Name = "${var.python_asia_talk}-private-route-table"
  }
  
}