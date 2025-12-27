resource "aws_instance" "python_asia_talk_ec2_instance" {
  ami = var.python_asia_talk_ec2_ami_id
  instance_type = var.python_asia_talk_ec2_instance_size
  associate_public_ip_address = true
  subnet_id = aws_subnet.python_asia_talk_private_subnet.id
  vpc_security_group_ids = [aws_security_group.ssh_ec2.id]
  
}