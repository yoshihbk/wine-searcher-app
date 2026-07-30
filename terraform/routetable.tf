# パブリックルートテーブルの作成（箱）
resource "aws_route_table" "public_route" {
  vpc_id = aws_vpc.wine_app_vpc.id

  tags = merge(
    var.default_tags,
    { Name = "${var.project}-public-route" }
  )
}

# パブリックルートの作成（道筋）
resource "aws_route" "public_internet" {
  route_table_id = aws_route_table.public_route.id
  # アウトバウンド
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id

}


# パブリックルートテーブルの紐づけ1a
resource "aws_route_table_association" "public_1a" {
  subnet_id      = aws_subnet.public_subnet_1a.id
  route_table_id = aws_route_table.public_route.id
}

# パブリックルートテーブルの紐づけ1c
resource "aws_route_table_association" "public_1c" {
  subnet_id      = aws_subnet.public_subnet_1c.id
  route_table_id = aws_route_table.public_route.id
}

# プライベートルートテーブルの作成
resource "aws_route_table" "private_route" {
  vpc_id = aws_vpc.wine_app_vpc.id

  tags = merge(
    var.default_tags,
    { Name = "${var.project}-private-route" }
  )
}



# Nat用ルートの作成
resource "aws_route" "nat" {
  route_table_id = aws_route_table.private_route.id
  # アウトバウンド
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.ngw.id

}
# Natルートテーブルの紐づけ1a
resource "aws_route_table_association" "private_1a" {
  subnet_id      = aws_subnet.private_subnet_1a.id
  route_table_id = aws_route_table.private_route.id
}

#Nat ルートテーブルの紐づけ1c
resource "aws_route_table_association" "private_1c" {
  subnet_id      = aws_subnet.private_subnet_1c.id
  route_table_id = aws_route_table.private_route.id
}