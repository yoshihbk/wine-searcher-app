resource "aws_vpc" "wine_app_vpc" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true
  instance_tenancy     = "default"
  tags = merge(
    var.default_tags,
    { Name = "${var.project}-vpc" }
  )
}