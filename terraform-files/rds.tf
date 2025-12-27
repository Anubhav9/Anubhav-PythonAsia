resource "aws_db_subnet_group" "python_asia_talk_db_subnet_group" {
  name = "python_asia_talk_db_subnet_group"
  subnet_ids = [aws_subnet.python_asia_talk_private_subnet.id,aws_subnet.python_asia_talk_private_subnet_2.id]
  tags = {
    Name = "${var.python_asia_talk}-db-subnet-group"
  }
  
}

resource "aws_db_instance" "python_asia_talk_rds_instance" {
  allocated_storage = var.python_asia_talk_db_storage
  db_name = "${var.python_asia_talk}-db"
  engine = "postgres"
  engine_version = "18.1"
  instance_class = "db.t3.micro"
  username = "custom_admin"
  password = var.python_asia_talk_db_password
  db_subnet_group_name = aws_db_subnet_group.python_asia_talk_db_subnet_group.name
  publicly_accessible = false
  multi_az = false
  vpc_security_group_ids = [aws_security_group.rds_security_group.id]
  tags ={
    Name = "${var.python_asia_talk}-database"
  }
  
}