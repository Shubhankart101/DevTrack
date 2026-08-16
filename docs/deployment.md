# Deployment

Application CI has two merge/build workflows plus an extended manual test workflow. Pull requests targeting `main` run tests automatically; the build, test, and deployment workflow and the extended test workflow are started manually. Infrastructure workflows remain manual.

## Application pipelines

| Workflow | Purpose |
| --- | --- |
| [pull-request-tests.yml](../.github/workflows/pull-request-tests.yml) | Run Django checks and all app tests for pull requests targeting `main` |
| [app-deploy.yml](../.github/workflows/app-deploy.yml) | Manually build, test, and optionally deploy the Django app via a GitHub-hosted runner |
| [extended-tests.yml](../.github/workflows/extended-tests.yml) | Run the expanded API scenario suite for every commit on every branch, every Saturday at 12:00 PM IST, or manually, without deploying |

The pull-request workflow runs on opened, reopened, and updated pull requests targeting `main`. Configure the `main` branch protection rules with these settings:

- Require a pull request before merging.
- Require the `Pull Request Tests / test` status check to pass.
- Require branches to be up to date before merging.
- Restrict direct pushes and force pushes to `main` to repository administrators only.
- Do not allow bypassing the pull-request requirement for normal contributors.

In GitHub, open **Settings → Branches → Add branch ruleset**, target `main`, enable the settings above, and set the ruleset to **Active**. This repository configuration is required to technically block direct commits; the workflow alone can only run the pre-merge checks.

## Infrastructure pipelines

| Workflow | Purpose |
| --- | --- |
| [publish-status-board.yml](../.github/workflows/publish-status-board.yml) | Manually publish the standalone GitHub Actions status board to GitHub Pages |
| [runner-infra.yml](../.github/workflows/runner-infra.yml) | Provision the Azure-hosted Linux runner VM |
| [azure-deploy.yml](../.github/workflows/azure-deploy.yml) | Provision or update Azure Web App infrastructure |
| [terraform.yml](../.github/workflows/terraform.yml) | Reusable Terraform template (called by the two infra pipelines) |

## Standalone pipeline status board

Open [status-board.html](status-board.html) directly for a server-free view of the latest public GitHub Actions runs. It polls GitHub every 15 seconds and links each run back to GitHub.

To publish it, run `publish-status-board.yml` manually and enable GitHub Pages with **GitHub Actions** as the source. The published board will be available at `https://OWNER.github.io/REPOSITORY/status-board.html`.

## Recommended order

1. Run **azure-deploy** with `terraform_action=apply`.
2. Run **app-deploy** manually to build, test, and deploy the Django application on `ubuntu-latest`.

## Test commands

From the repository root, install dependencies and run the same checks used by the application pipelines:

```bash
pip install -r requirements.txt
python devtrack/manage.py check
python devtrack/manage.py test issues
```

The test suite is located at `devtrack/issues/tests.py` and uses temporary JSON files, so it does not modify the development fixtures.

## Self-hosted runner infrastructure

The repository still contains the optional Azure self-hosted runner infrastructure for a future migration. The application workflows currently use GitHub-hosted `ubuntu-latest` runners, so provisioning the runner is not required for normal application builds, tests, or deployments.

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
