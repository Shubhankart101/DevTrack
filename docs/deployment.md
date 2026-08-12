# Deployment

All pipelines are `workflow_dispatch` only — nothing runs automatically.

## Pipelines

| Workflow | Purpose |
| --- | --- |
| [runner-infra.yml](../.github/workflows/runner-infra.yml) | Provision the Azure-hosted Linux runner VM |
| [azure-deploy.yml](../.github/workflows/azure-deploy.yml) | Provision or update Azure Web App infrastructure |
| [app-deploy.yml](../.github/workflows/app-deploy.yml) | Build and deploy the Django app via the self-hosted runner |
| [terraform.yml](../.github/workflows/terraform.yml) | Reusable Terraform template (called by the two infra pipelines) |

## Recommended order

1. Run **runner-infra** with `terraform_action=apply`.
2. Confirm the runner is online in Actions → Runners in the repository settings.
3. Run **azure-deploy** with `terraform_action=apply`.
4. Run **app-deploy** to deploy the Django application.

## Self-hosted runner

The runner VM runs Ubuntu 22.04 (`Standard_B2s`) on Azure. It registers with the labels `self-hosted`, `linux`, `azure`, and `devtrack`. The app deployment job targets those labels.

## Terraform structure

```
infra/terraform/           # Web App infrastructure root
infra/terraform/runner/    # Runner VM infrastructure root
infra/terraform/modules/
  resource_group/          # Azure resource group
  service_plan/            # Azure App Service plan
  linux_web_app/           # Azure Linux Web App
  github_runner_vm/        # Azure Linux VM + VNet + NIC + cloud-init runner bootstrap
```

## Required GitHub secrets

| Secret | Purpose |
| --- | --- |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription |
| `AZURE_TENANT_ID` | Azure tenant |
| `AZURE_CLIENT_ID` | Service principal client ID |
| `AZURE_CLIENT_SECRET` | Service principal secret |
| `AZURE_WEBAPP_NAME` | Target Azure Web App name |
| `AZURE_PUBLISH_PROFILE` | Publish profile for app deployment |
| `AZURE_RUNNER_SSH_PUBLIC_KEY` | Public SSH key for the runner VM admin account |
| `GH_RUNNER_ADMIN_TOKEN` | Token with permission to create runner registration tokens for this repository |
