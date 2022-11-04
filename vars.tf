variable "region" {
  default = "eu-west-2"
}

provider "aws" {
  region = var.region
}
