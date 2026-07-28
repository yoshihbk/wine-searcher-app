variable "cidr_block" {
  description = "VPCのcidrブロックを指定します"
}

variable "project" {
  type        = string
  description = "Wine-Searcher"
}

variable "default_tags" {
  type = map(string)

}

variable "public_subnet_cidr_1a" {
  description = "パブリックサブネット1aのcidr範囲"
}

variable "public_subnet_cidr_1c" {
  description = "パブリックサブネット1cのcidr範囲"
}

variable "private_subnet_cidr_1a" {
  description = "プライベートサブネット1aのcidr範囲"
}

variable "private_subnet_cidr_1c" {
  description = "プライベートサブネット1cのcidr範囲"
}

