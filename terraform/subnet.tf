# パブリックサブネットAの作成
resource "aws_subnet" "public_subnet_1a" {
  availability_zone = "ap-northeast-1a"
  vpc_id            = aws_vpc.wine_app_vpc.id
  cidr_block        = var.public_subnet_cidr_1a
  tags = merge(
    var.default_tags,
    { Name = "${var.project}-public-subnet-1a" }
  )
}