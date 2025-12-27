resource "aws_subnet" "python_asia_talk_public_subnet" {
  vpc_id = aws_vpc.vpc_python_asia_talk.id
  cidr_block = var.python_asia_talk_public_subet_cidr
  map_public_ip_on_launch = true
  tags = {
    Name = "${var.python_asia_talk}-public-subnet"
  }
  
}

resource "aws_subnet" "python_asia_talk_private_subnet" {
  vpc_id = aws_vpc.vpc_python_asia_talk.id
  cidr_block = var.python_asia_talk_private_subnet_cidr
  availability_zone_id = "apne3-az1"
  tags = {
    Name = "${var.python_asia_talk}-private_subnet"
  }
  
}

resource "aws_subnet" "python_asia_talk_private_subnet_2" {
  vpc_id = aws_vpc.vpc_python_asia_talk.id
  cidr_block = var.python_asia_talk_private_subnet_cidr_2
  availability_zone_id = "apne3-az2"
  tags = {
    Name = "${var.python_asia_talk}-private_subnet_2"
  }
  
}


resource "aws_route_table_association" "python_asia_talk_public_subnet_route_table_association" {
  subnet_id = aws_subnet.python_asia_talk_public_subnet.id
  route_table_id = aws_route_table.python_asia_talk_public_route_table.id
  
  
}

resource "aws_route_table_association" "python_asia_talk_private_route_table_association" {
  subnet_id = aws_subnet.python_asia_talk_private_subnet.id
  route_table_id = aws_route_table.python_asia_talk_private_route_table.id
  
  
}

resource "aws_route_table_association" "python_asia_talk_private_route_table_association_2" {
  subnet_id = aws_subnet.python_asia_talk_private_subnet_2.id
  route_table_id = aws_route_table.python_asia_talk_private_route_table.id
  
  
}