variable "name" {
  description = "Name of the Azure Linux Web App"
  type        = string
}

variable "location" {
  description = "Azure region for the Linux Web App"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group name that owns the Linux Web App"
  type        = string
}

variable "service_plan_id" {
  description = "App Service plan ID for the Linux Web App"
  type        = string
}

variable "python_version" {
  description = "Python runtime version for the Linux Web App"
  type        = string
}