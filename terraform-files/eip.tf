resource "aws_eip" "python_asia_talk_eip" {
  domain = "vpc"
  tags = {
    Name = "${var.python_asia_talk}-eip"
  }
  
}