# Deployment

Application CI has two merge/build workflows plus an extended manual test workflow. Pull requests targeting `main` run tests automatically; the build, test, and deployment workflow and the extended test workflow are started manually. Infrastructure workflows remain manual. See [README.md](README.md) for pipeline failure modes and mitigations.

## Application pipelines

Use the active [GitHub Actions pipeline-runs dashboard](https://github.com/Shubhankart101/DevTrack/actions) to inspect workflow status, expanded stages, and logs. The custom live tracker is retired and should not be used.

| Workflow | Purpose |
| --- | --- |
| [pull-request-tests.yml](../.github/workflows/pull-request-tests.yml) | Run Django checks and all app tests for pull requests targeting `main` |
| [app-deploy.yml](../.github/workflows/app-deploy.yml) | Manually build, test, and optionally deploy the Django app via a GitHub-hosted runner |
| [extended-tests.yml](../.github/workflows/extended-tests.yml) | Run the expanded API scenario suite for code-changing commits on every branch, every Saturday at 12:00 PM IST, or manually, without deploying |

Automatic pull-request and branch-push test runs skip changes that affect only `README.md` files. Changes to code still trigger them; manual and scheduled runs remain available.

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

The standalone [status-board.html](status-board.html) dashboard is published through GitHub Pages and can also be run locally. Use [status-board.md](status-board.md) for setup and branch-specific URLs.

The preserved dashboard code uses entertaining GIFs as status controls: `office.gif` filters failed runs, `bounce-dwight.gif` filters running runs, and `great-job.gif` filters succeeded runs. It is currently inactive.

<img src="assets/office.gif" width="560" alt="Office team reaction"><br>Failed pipeline: investigate the run.

<img src="assets/bounce-dwight.gif" width="560" alt="Dwight bouncing"><br>Running pipeline: checks are in motion.

<img src="assets/great-job.gif" width="560" alt="Great job"><br>Succeeded pipeline: ready to celebrate.

The [status-board.html](status-board.html) dashboard is published through GitHub Pages and can also be run locally. Click a run to expand its stages, then click a stage to load its inline log.

Before running the publisher, ensure GitHub Pages is configured with **GitHub Actions** as the source. The default repository token cannot create the Pages site. If raw stage logs are restricted in the browser, use the direct GitHub job-log link.

### Dashboard recovery

If the publisher fails, inspect the latest **Publish Pipeline Status Board** run in **Actions** and rerun it after fixing the reported step. A `configure-pages` failure means Pages is not enabled with **GitHub Actions** as its source.

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
