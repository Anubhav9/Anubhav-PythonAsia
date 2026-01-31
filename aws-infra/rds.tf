resource "aws_db_subnet_group" "python_asia_db_subnet_group" {
  name = "python_asia_db_subnet_group"
  subnet_ids = [aws_subnet.python_asia_private_subnet.id,aws_subnet.python_asia_private_subnet_2.id]
  tags = {
    Name = "${var.python_asia_nomenclature}-db-subnet-group"
  }
  
}

resource "aws_db_instance" "python_asia_talk_rds_instance" {
  allocated_storage = 20
  db_name = "pythonasiadb"
  engine = "postgres"
  engine_version = "18.1"
  instance_class = "db.t3.micro"
  username = "custom_admin"
  password = var.python_asia_db_password
  db_subnet_group_name = aws_db_subnet_group.python_asia_db_subnet_group.name
  publicly_accessible = false
  multi_az = false
  vpc_security_group_ids = [aws_security_group.python_asia_rds_security_group.id]
  tags ={
    Name = "${var.python_asia_nomenclature}-database"
  }
  skip_final_snapshot = true
  
}