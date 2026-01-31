resource "aws_security_group" "python_asia_ec2_security_group" {
  vpc_id = aws_vpc.python_asia_vpc.id
  name = "EC2 Security Group"
  description = "Allow SSH into EC2 instance"
  
}

resource "aws_vpc_security_group_ingress_rule" "python_asia_ec2_ingress_rule" {
  security_group_id = aws_security_group.python_asia_ec2_security_group.id
  cidr_ipv4 = "0.0.0.0/0"
  from_port = 22
  to_port = 22
  ip_protocol = "tcp"
  
}

resource "aws_vpc_security_group_egress_rule" "python_asia_ec2_egress_rule" {
  security_group_id = aws_security_group.python_asia_ec2_security_group.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}

resource "aws_security_group" "python_asia_rds_security_group" {
  vpc_id = aws_vpc.python_asia_vpc.id
  name = "RDS Security Group"
  description = "Allow Ingress into RDS"
  
}

resource "aws_vpc_security_group_ingress_rule" "python_asia_rds_ingress_rule" {
  security_group_id = aws_security_group.python_asia_rds_security_group.id
  referenced_security_group_id = aws_security_group.python_asia_ec2_security_group.id
  from_port = 5432
  to_port = 5432
  ip_protocol = "tcp"
  
}