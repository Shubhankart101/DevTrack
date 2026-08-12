variable "name" {
  description = "Name of the Azure App Service plan"
  type        = string
}

variable "location" {
  description = "Azure region for the App Service plan"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group name that owns the App Service plan"
  type        = string
}

variable "sku_name" {
  description = "SKU for the Azure App Service plan"
  type        = string
}