variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
}

variable "tenant_id" {
  description = "Azure tenant ID"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus"
}

variable "resource_group_name" {
  description = "Runner resource group name"
  type        = string
  default     = "rg-devtrack-runner"
}

variable "virtual_network_name" {
  description = "Runner virtual network name"
  type        = string
  default     = "vnet-devtrack-runner"
}

variable "virtual_network_cidr" {
  description = "Runner virtual network address space"
  type        = string
  default     = "10.20.0.0/16"
}

variable "subnet_name" {
  description = "Runner subnet name"
  type        = string
  default     = "snet-devtrack-runner"
}

variable "subnet_cidr" {
  description = "Runner subnet address prefix"
  type        = string
  default     = "10.20.1.0/24"
}

variable "public_ip_name" {
  description = "Runner public IP name"
  type        = string
  default     = "pip-devtrack-runner"
}

variable "network_security_group_name" {
  description = "Runner network security group name"
  type        = string
  default     = "nsg-devtrack-runner"
}

variable "network_interface_name" {
  description = "Runner network interface name"
  type        = string
  default     = "nic-devtrack-runner"
}

variable "vm_name" {
  description = "Runner VM name"
  type        = string
  default     = "vm-devtrack-runner"
}

variable "vm_size" {
  description = "Runner VM size"
  type        = string
  default     = "Standard_B2s"
}

variable "admin_username" {
  description = "Runner VM admin username"
  type        = string
  default     = "azureuser"
}

variable "admin_ssh_public_key" {
  description = "SSH public key used to manage the runner VM"
  type        = string
}

variable "admin_allowed_cidr" {
  description = "Optional CIDR allowed to SSH into the runner VM"
  type        = string
  default     = null
}

variable "github_repository" {
  description = "Repository in owner/name format for the self-hosted runner"
  type        = string
}

variable "github_runner_name" {
  description = "Name presented by the self-hosted runner"
  type        = string
  default     = "devtrack-runner"
}

variable "github_runner_labels" {
  description = "Comma-separated labels assigned to the self-hosted runner"
  type        = string
  default     = "azure,devtrack"
}

variable "github_runner_registration_token" {
  description = "Short-lived token used to register the self-hosted runner"
  type        = string
  sensitive   = true
}

variable "runner_version" {
  description = "GitHub Actions runner version"
  type        = string
  default     = "2.328.0"
}