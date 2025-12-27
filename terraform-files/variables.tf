variable "vpc_cidr_block" {
  type = string
  description = "default CIDR block for VPC"
  default = "10.0.0.0/20"
}

variable "python_asia_talk" {
  type = string
  description = "nomenclature for anything related to Python Asia"
  default = "python-asia-talk"
}

variable "python_asia_talk_public_subet_cidr" {
  type = string
  description = "CIDR for public subnet for Python Asia Talk"
  default = "10.0.0.0/26"
}

variable "python_asia_talk_private_subnet_cidr" {
  type = string
  description = "CIDR for private subnet for Python Asia Talk"
  default = "10.0.1.0/24"
}
variable "python_asia_talk_private_subnet_cidr_2" {
  type = string
  description = "CIDR for private subnet for Python Asia Talk"
  default = "10.0.2.0/24"
}

variable "python_asia_talk_public_route" {
  type = string
  description = "Public Internet Route"
  default = "0.0.0.0/0"
}

variable "python_asia_talk_db_storage" {
  type = number
  description = "DB Storage in GBs"
  default = 10
}

variable "python_asia_talk_db_password" {
  type = string
  description = "Password for the DB"
  sensitive = true
}

variable "python_asia_talk_ec2_ami_id" {
  type = string
  description = "AMI ID of the EC2 instance"
  default = "ami-09a38e2e7a3cc42de"
}

variable "python_asia_talk_ec2_instance_size" {
  type = string
  description = "describe your variable"
  default = "t3.micro"
}