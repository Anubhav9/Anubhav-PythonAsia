resource "aws_instance" "python_asia_jumbox" {
  ami = var.ami_ec2
  instance_type = var.instance_size_ec2
  subnet_id = aws_subnet.python_asia_public_subnet.id
  key_name = "PythonAsiaTalkKeyValuePair"
  vpc_security_group_ids = [aws_security_group.python_asia_ec2_security_group.id]

  associate_public_ip_address = true

  tags = {
    Name = "python-asia-jumpbox"
  }

  
}