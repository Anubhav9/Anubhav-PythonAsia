variable "vpc_cidr_block" {
  type = string
  description = "CIDR Block"
  default = "10.0.16.0/20"
}

variable "python_asia_nomenclature" {
  type = string
  description = "Nomenclature Convention for Python Asia"
  default = "python-asia"
}

variable "private_subnet_cidr" {
  type = string
  description = "CIDR block for Private Subnet"
  default = "10.0.20.0/24"
}

variable "private_subnet_cidr_2" {
  type = string
  description = "CIDR block for Private Subnet"
  default = "10.0.21.0/24"
}

variable "public_subnet_cidr" {
  type = string
  description = "CIDR block for Public Subnet"
  default = "10.0.16.0/22"
}

variable "availability_zone_1" {
  type = string
  description = "Availability Zone 1"
  default = "ap-northeast-3a"
}

variable "availability_zone_2" {
  type = string
  description = "Availability Zone 1"
  default = "ap-northeast-3b"
}

variable "ami_ec2" {
  type = string
  description = "AMI for EC2 instance"
  default = "ami-09a38e2e7a3cc42de"
}

variable "instance_size_ec2" {
  type = string
  description = "Size for EC2 Instance Jump Box"
  default = "t3.micro"
}

variable "python_asia_db_password" {
  type = string
  description = "RDS Password"
}

