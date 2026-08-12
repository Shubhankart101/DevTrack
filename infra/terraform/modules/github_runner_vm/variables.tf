variable "location" {
  description = "Azure region for the runner resources"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group that owns the runner resources"
  type        = string
}

variable "virtual_network_name" {
  description = "Virtual network name for the runner"
  type        = string
}

variable "virtual_network_cidr" {
  description = "Address space for the runner virtual network"
  type        = string
}

variable "subnet_name" {
  description = "Subnet name for the runner"
  type        = string
}

variable "subnet_cidr" {
  description = "Address prefix for the runner subnet"
  type        = string
}

variable "public_ip_name" {
  description = "Public IP resource name for the runner VM"
  type        = string
}

variable "network_security_group_name" {
  description = "Network security group name for the runner VM"
  type        = string
}

variable "network_interface_name" {
  description = "Network interface name for the runner VM"
  type        = string
}

variable "vm_name" {
  description = "Virtual machine name for the runner"
  type        = string
}

variable "vm_size" {
  description = "VM size for the runner"
  type        = string
}

variable "admin_username" {
  description = "Admin username for the runner VM"
  type        = string
}

variable "admin_ssh_public_key" {
  description = "SSH public key for the runner VM"
  type        = string
}

variable "admin_allowed_cidr" {
  description = "Optional CIDR allowed to SSH to the runner VM"
  type        = string
  default     = null
}

variable "github_repository" {
  description = "Repository in owner/name format for runner registration"
  type        = string
}

variable "github_runner_name" {
  description = "GitHub Actions runner name"
  type        = string
}

variable "github_runner_labels" {
  description = "Comma-separated labels assigned to the runner"
  type        = string
}

variable "github_runner_registration_token" {
  description = "Short-lived registration token used to configure the runner"
  type        = string
  sensitive   = true
}

variable "runner_version" {
  description = "GitHub Actions runner version"
  type        = string
}