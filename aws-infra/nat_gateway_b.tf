resource "aws_nat_gateway" "python_asia_nat_gateway" {
  allocation_id = aws_eip.python_asia_elastic_ip.id
  subnet_id = aws_subnet.python_asia_public_subnet.id
  depends_on = [aws_internet_gateway.python_asia_internet_gateway]
  tags = {
    Name = "${var.python_asia_nomenclature}-nat-gateway"
  }
  
}