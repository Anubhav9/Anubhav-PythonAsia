resource "aws_security_group" "ssh_ec2" {
  name = "Allow SSH EC2"
  description = "Allowing SSH into EC2 instance from Public Internet"
  vpc_id = aws_vpc.vpc_python_asia_talk.id
  tags ={
    Name = "${var.python_asia_talk}-ssh-ec2-sg"
  }
  
}

resource "aws_vpc_security_group_ingress_rule" "allow_ssh" {
  security_group_id = aws_security_group.ssh_ec2.id
  cidr_ipv4 = var.python_asia_talk_public_route
  from_port = 22
  to_port = 22
  ip_protocol = "tcp"
}

resource "aws_security_group" "rds_security_group" {
  name = "Security Group for RDS"
  description = "What needs to be allowed to RDS"
  vpc_id = aws_vpc.vpc_python_asia_talk.id
  tags ={
    Name = "${var.python_asia_talk}-rds-sg"
  }
  
}

resource "aws_vpc_security_group_ingress_rule" "allowed_to_connect_to_rds" {
  security_group_id = aws_security_group.rds_security_group.id
  referenced_security_group_id = aws_security_group.ssh_ec2.id
  ip_protocol = "tcp"
  from_port = 5432
  to_port = 5432
  
}