## Terraform Pipelines

This repository now uses one reusable Terraform workflow template with two manual entrypoints:

- `.github/workflows/azure-deploy.yml` provisions the Azure Web App infrastructure from `infra/terraform`
- `.github/workflows/runner-infra.yml` provisions the Azure-hosted GitHub Actions runner from `infra/terraform/runner`

<img src="../../docs/assets/atg-studiocapa.gif" width="560" alt="Extra momentum">

### Required GitHub secrets

- `AZURE_SUBSCRIPTION_ID`
- `AZURE_TENANT_ID`
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `AZURE_WEBAPP_NAME`
- `AZURE_PUBLISH_PROFILE`
- `AZURE_RUNNER_SSH_PUBLIC_KEY`
- `GH_RUNNER_ADMIN_TOKEN`

`GH_RUNNER_ADMIN_TOKEN` needs permission to create self-hosted runner registration tokens for this repository. `AZURE_RUNNER_SSH_PUBLIC_KEY` should contain the public key for the VM admin account.

<img src="../../docs/assets/eyebrow-raise-dwight.gif" width="560" alt="Careful review">

The runner workflow registers a repository-scoped Linux runner with the built-in `self-hosted` and `linux` labels plus the custom `azure` and `devtrack` labels.

<img src="../../docs/assets/the-office-the-office-memes.gif" width="560" alt="Office pipeline reaction">

### Recommended order

1. Run `.github/workflows/runner-infra.yml` with `terraform_action=apply`.
2. Wait for the runner to appear online in the repository's Actions runner settings.
3. Run `.github/workflows/azure-deploy.yml` to provision or update the hosting infra.

<img src="../../docs/assets/hell-yeah-yeah.gif" width="560" alt="Green build celebration">

4. Run `.github/workflows/app-deploy.yml` to deploy the Django application on the self-hosted runner.

<img src="../../docs/assets/crazy-dance-funny-dance.gif" width="560" alt="Build celebration">

Use the [pipeline status board](../../docs/status-board.md) to expand the infrastructure run, click each Terraform stage to load its inline log, and open the full GitHub job log for failures.

## Pipeline GIF gallery

<img src="../../docs/assets/devtrack-code-loop.gif" width="560" alt="DevTrack code loop">

<img src="../../docs/assets/office.gif" width="560" alt="Office team ready">

<img src="../../docs/assets/bounce-dwight.gif" width="560" alt="Dwight bouncing">

<img src="../../docs/assets/great-job.gif" width="560" alt="Great job">

<img src="../../docs/assets/thats-what-she-said-what-she-said.gif" width="560" alt="That's what she said">

<img src="../../docs/assets/tired-office.gif" width="560" alt="Tired Office">

<img src="../../docs/assets/pipeline-queued.gif" width="560" alt="Pipeline queued">

<img src="../../docs/assets/pipeline-running.gif" width="560" alt="Pipeline running">

<img src="../../docs/assets/pipeline-success.gif" width="560" alt="Pipeline passed">

<img src="../../docs/assets/pond-naravit-ppnaravit.gif" width="560" alt="Surprising pipeline result">