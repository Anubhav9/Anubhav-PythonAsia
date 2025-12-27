resource "aws_nat_gateway" "python_asia_talk_nat_gateway" {
  allocation_id = aws_eip.python_asia_talk_eip.id
  subnet_id = aws_subnet.python_asia_talk_public_subnet.id
  tags = {
    Name = "${var.python_asia_talk}-nat-gateway"
  }
  depends_on = [aws_internet_gateway.python_asia_talk_internet_gateway]
  
}