variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
}

variable "tenant_id" {
  description = "Azure tenant ID"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the Azure resource group"
  type        = string
  default     = "rg-devtrack"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus"
}

variable "app_service_plan_name" {
  description = "Azure App Service plan name"
  type        = string
  default     = "plan-devtrack"
}

variable "app_service_plan_sku" {
  description = "Azure App Service plan SKU"
  type        = string
  default     = "B1"
}

variable "app_name" {
  description = "Azure Web App name"
  type        = string
}

variable "python_version" {
  description = "Python runtime version for the Azure Web App"
  type        = string
  default     = "3.12"
}
