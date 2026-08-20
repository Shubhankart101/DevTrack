terraform {
  required_version = ">= 1.5.0"

  backend "azurerm" {
    resource_group_name  = "REPLACE_ME"
    storage_account_name = "REPLACE_ME"
    container_name       = "tfstate"
    key                  = "project/environment.tfstate"
  }
}

resource "terraform_data" "state_example" {
  input = "remote-state-enabled"
}
