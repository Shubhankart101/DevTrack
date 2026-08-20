terraform {
  required_version = ">= 1.5.0"
}

variable "environments" {
  type        = set(string)
  description = "Environments to model"
  default     = ["dev", "test", "prod"]

  validation {
    condition     = length(var.environments) > 0
    error_message = "At least one environment is required."
  }
}

variable "sku_by_environment" {
  type        = map(string)
  description = "Example SKU map"
  default = {
    dev  = "basic"
    test = "standard"
    prod = "premium"
  }
}

resource "terraform_data" "environment" {
  for_each = var.environments
  input    = "${each.key}-${lookup(var.sku_by_environment, each.key, "standard")}"
}

output "environment_values" {
  value = { for name, item in terraform_data.environment : name => item.output }
}
