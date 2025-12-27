resource "aws_internet_gateway" "python_asia_talk_internet_gateway" {
  vpc_id = aws_vpc.vpc_python_asia_talk.id
  tags = {
    Name = "${var.python_asia_talk}-igw"
  }
  
}