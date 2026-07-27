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