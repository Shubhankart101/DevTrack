terraform {
  required_version = ">= 1.5.0"
}

variable "platform" {
  type        = string
  description = "Platform name"
  default     = "shared-platform"
}

variable "components" {
  type        = map(object({ owner = string, criticality = string }))
  description = "Platform components"
  default = {
    network = { owner = "platform", criticality = "high" }
    app     = { owner = "product", criticality = "high" }
    data    = { owner = "data", criticality = "medium" }
  }
}

locals {
  component_names = sort(keys(var.components))
  component_tags = {
    for name, component in var.components : name => merge(component, {
      platform = var.platform
      component = name
    })
  }
}

resource "terraform_data" "component" {
  for_each = local.component_tags
  input    = jsonencode(each.value)
}

output "platform_components" {
  value = { for name, component in terraform_data.component : name => component.output }
}
