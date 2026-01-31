resource "aws_route_table" "python_asia_public_subnet_route_table" {
  vpc_id = aws_vpc.python_asia_vpc.id
}

resource "aws_route" "python_asia_public_subnet_route" {
  route_table_id = aws_route_table.python_asia_public_subnet_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.python_asia_internet_gateway.id
  
}

resource "aws_route_table" "python_asia_private_subnet_route_table" {
  vpc_id = aws_vpc.python_asia_vpc.id
  
}

resource "aws_route" "python_asia_private_subnet_route" {
  route_table_id = aws_route_table.python_asia_private_subnet_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id = aws_nat_gateway.python_asia_nat_gateway.id
  
}