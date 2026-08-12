module "resource_group" {
  source = "../modules/resource_group"

  name     = var.resource_group_name
  location = var.location
}

module "github_runner_vm" {
  source = "../modules/github_runner_vm"

  location                         = module.resource_group.location
  resource_group_name              = module.resource_group.name
  virtual_network_name             = var.virtual_network_name
  virtual_network_cidr             = var.virtual_network_cidr
  subnet_name                      = var.subnet_name
  subnet_cidr                      = var.subnet_cidr
  public_ip_name                   = var.public_ip_name
  network_security_group_name      = var.network_security_group_name
  network_interface_name           = var.network_interface_name
  vm_name                          = var.vm_name
  vm_size                          = var.vm_size
  admin_username                   = var.admin_username
  admin_ssh_public_key             = var.admin_ssh_public_key
  admin_allowed_cidr               = var.admin_allowed_cidr
  github_repository                = var.github_repository
  github_runner_name               = var.github_runner_name
  github_runner_labels             = var.github_runner_labels
  github_runner_registration_token = var.github_runner_registration_token
  runner_version                   = var.runner_version
}