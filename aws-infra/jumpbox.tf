data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

resource "aws_instance" "python_asia_jumbox" {
  ami                    = data.aws_ami.amazon_linux_2023.id
  instance_type          = var.instance_size_ec2
  subnet_id              = aws_subnet.python_asia_public_subnet.id
  key_name               = "PythonAsiaTalkKeyValuePair"
  vpc_security_group_ids = [aws_security_group.python_asia_ec2_security_group.id]

  associate_public_ip_address = true

  tags = {
    Name = "python-asia-jumpbox"
  }


}
