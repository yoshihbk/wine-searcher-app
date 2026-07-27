variable "cidr_block" {
  description = "VPCのcidrブロックを指定します"
}

variable "public_subnet_cidr_1a" {
  description = "パブリックサブネット1aのcidr範囲"
}


variable "project" {
  type        = string
  description = "Wine-Searcher"
}

variable "default_tags" {
  type = map(string)

}

