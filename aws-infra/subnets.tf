resource "aws_subnet" "python_asia_private_subnet" {
  vpc_id = aws_vpc.python_asia_vpc.id
  cidr_block = var.private_subnet_cidr
  availability_zone = var.availability_zone_1
  tags = {
    Name = "${var.python_asia_nomenclature}-private-subnet"
  }
  
}

resource "aws_subnet" "python_asia_private_subnet_2" {
  vpc_id = aws_vpc.python_asia_vpc.id
  cidr_block = var.private_subnet_cidr_2
  availability_zone = var.availability_zone_2
  tags = {
    Name = "${var.python_asia_nomenclature}-private-subnet-2"
  }
  
}


resource "aws_subnet" "python_asia_public_subnet" {
  vpc_id = aws_vpc.python_asia_vpc.id
  cidr_block = var.public_subnet_cidr
  availability_zone = var.availability_zone_2
  map_public_ip_on_launch = true
  tags = {
    Name = "${var.python_asia_nomenclature}-public-subnet"
  }

  
}

resource "aws_route_table_association" "python_asia_public_subnet_route_table_association" {
  subnet_id = aws_subnet.python_asia_public_subnet.id
  route_table_id = aws_route_table.python_asia_public_subnet_route_table.id
  
}

resource "aws_route_table_association" "python_asia_private_subnet_route_table_association" {
  subnet_id = aws_subnet.python_asia_private_subnet.id
  route_table_id = aws_route_table.python_asia_private_subnet_route_table.id
  
}

resource "aws_route_table_association" "python_asia_private_subnet_route_table_association_2" {
  subnet_id = aws_subnet.python_asia_private_subnet_2.id
  route_table_id = aws_route_table.python_asia_private_subnet_route_table.id
  
}