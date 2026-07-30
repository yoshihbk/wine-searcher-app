resource "aws_security_group" "wine_alb_sg" {
  name        = "${var.project}-alb_sg"
  description = "Allow TLS inbound traffic and all outbound traffic"
  vpc_id      = aws_vpc.wine_app_vpc.id
  # タグのマージ
  tags = merge(
    var.default_tags,
    { Name = "${var.project}-alb_sg" }
  )
}

resource "aws_vpc_security_group_ingress_rule" "wine_alb_ingress_rule_ipv4" {
  security_group_id = aws_security_group.wine_alb_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  ip_protocol       = "tcp"
  to_port           = 80
}

resource "aws_vpc_security_group_ingress_rule" "wine_alb_ingress_rule_ipv6" {
  security_group_id = aws_security_group.wine_alb_sg.id
  cidr_ipv6         = "::/0"
  from_port         = 443
  ip_protocol       = "tcp"
  to_port           = 443
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv4" {
  security_group_id = aws_security_group.wine_alb_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv6" {
  security_group_id = aws_security_group.wine_alb_sg.id
  cidr_ipv6         = "::/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}