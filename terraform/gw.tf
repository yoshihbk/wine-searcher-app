# インターネットゲートウェイの作成
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.wine_app_vpc.id

  tags = merge(
    var.default_tags,
    { Name = "${var.project}-igw" }
  )
}

# natゲートウェイの作成
resource "aws_nat_gateway" "ngw" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public_subnet_1a.id

  tags = merge(
    var.default_tags,
    { Name = "${var.project}-nat-gw" }
  )

}

resource "aws_eip" "nat_eip" {
  tags = merge(
    var.default_tags,
    { Name = "${var.project}-nat-eip" }
  )
}
