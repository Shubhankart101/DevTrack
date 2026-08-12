output "web_app_url" {
  value = "https://${module.linux_web_app.default_hostname}"
}

output "resource_group_name" {
  value = module.resource_group.name
}
