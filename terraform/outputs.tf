output "vpc_id" {
  value       = aws_vpc.wine_app_vpc
  description = "作成されたVPCのID"
}

output "vpc_cidr_block" {
  value       = aws_vpc.wine_app_vpc.cidr_block
  description = "作成されたVPCのCIDRブロック"

}

output "public_subnet_1a" {
  value       = aws_subnet.public_subnet_1a
  description = "パブリックサブネット1aのID"

}