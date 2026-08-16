# Pipeline troubleshooting guide

This guide explains what should run for each kind of change in DevTrack, what can fail, and how to recover. All workflow paths below are relative to the repository root.

## Quick decision table

| Change set | Automatic workflow behavior | Manual workflow to use |
| --- | --- | --- |
| Python, Django, API, or test code | Pull-request tests and branch extended tests run | `app-deploy.yml` for a full build and deployment |
| Only a `README.md` file | Automatic pull-request and push tests are skipped | Run a workflow manually if validation is still required |
| Code plus a `README.md` file | Automatic tests run because the change includes code | Use the normal code workflow sequence |
| `docs/status-board.html`, `docs/index.html`, or `docs/assets/` | Published dashboard content | Run `publish-status-board.yml` manually to update Pages |
| Terraform app infrastructure | No automatic infrastructure run | Run `azure-deploy.yml` with `plan` or `apply` |
| Terraform runner infrastructure | No automatic infrastructure run | Run `runner-infra.yml` with `plan` or `apply` |
| Workflow YAML changes | The changed workflow may not trigger itself | Run that workflow manually or make a small code change to exercise it |

## Pipeline map

The active custom pipeline-runs dashboard is the [DevTrack GitHub Pages tracker](https://shubhankart101.github.io/DevTrack/status-board.html?repo=Shubhankart101%2FDevTrack). The native [GitHub Actions dashboard](https://github.com/Shubhankart101/DevTrack/actions) remains available for full logs.

- [Pull Request Tests](../.github/workflows/pull-request-tests.yml) runs Django checks and the complete test suite for pull requests targeting `main`.
- [Extended Manual Tests](../.github/workflows/extended-tests.yml) runs on code-changing pushes, Saturdays at 12:00 PM IST, or manual dispatch.
- [Build, Test, and Deploy](../.github/workflows/app-deploy.yml) is manual and compiles, checks, tests, and optionally deploys the app.
- [Provision App Infrastructure](../.github/workflows/azure-deploy.yml) is manual and calls the reusable Terraform workflow for `infra/terraform`.
- [Provision GitHub Runner Infrastructure](../.github/workflows/runner-infra.yml) is manual and calls the reusable Terraform workflow for `infra/terraform/runner`.
- [Publish Pipeline Status Board](../.github/workflows/publish-status-board.yml) manually publishes the tracker to GitHub Pages.

## Code changes

### Tests do not start

<img src="assets/office.gif" width="560" alt="Office team reaction"><br>First check whether the change was intentionally filtered.

**Likely causes:** The change only touched `README.md`, the pull request targets a branch other than `main`, the workflow is disabled, or the GitHub event was filtered.

**Mitigation:** Confirm the pull request base is `main`. Check the Actions tab and the changed-files list. For README-only work, skipped execution is expected. Use **Run workflow** when a manual validation is needed.

### Tests fail at checkout

**Likely causes:** A bad commit reference, an unavailable branch, or a temporary GitHub Actions outage.

**Mitigation:** Confirm the branch exists and rerun the workflow. Check the Actions status page if repeated checkout failures occur.

### Dependency installation fails

**Likely causes:** An invalid package version, Python-version incompatibility, a transient package-index outage, or a broken `requirements.txt` change.

**Mitigation:** Reproduce locally with `python -m pip install --upgrade pip` and `pip install -r requirements.txt`. Pin compatible versions, keep Python at 3.12 unless intentionally changing it, and rerun after a transient network failure.

### `compileall` fails

**Likely causes:** Python syntax errors, invalid indentation, or a malformed file under `devtrack/`.

**Mitigation:** Run `python -m compileall -q devtrack` locally. Fix the reported file before rerunning the pipeline.

### Django check fails

**Likely causes:** Incorrect settings, URL imports, missing app configuration, invalid view code, or a command run from the wrong directory.

**Mitigation:** From the repository root run `python devtrack/manage.py check`. Keep the working directory at the repository root and confirm the active Python environment contains Django.

### Unit or API tests fail

<img src="assets/bounce-dwight.gif" width="560" alt="Dwight bouncing"><br>One failing assertion can stop the whole test stage.

**Likely causes:** A changed response shape, validation rule, JSON fixture, route, persistence behavior, or test assumption.

**Mitigation:** Run `python devtrack/manage.py test issues` locally, then run the failing test by name. Do not modify committed JSON fixtures to make a test pass; tests should isolate temporary data.

### An extended scenario fails

**Likely causes:** The scenario is testing a specific endpoint contract such as duplicate IDs, invalid JSON, status filtering, missing reporters, or unsupported methods.

**Mitigation:** Read the scenario name in the workflow log, reproduce it with the matching test command, and verify the API status code and JSON error body against [api.md](api.md).

## README-only and documentation changes

The automatic `pull_request` and branch `push` triggers use:

```yaml
paths-ignore:
  - '**/README.md'
```

This means:

- A README-only commit does not start those automatic test workflows.
- A commit containing code and a README starts them.
- Manual dispatch and the scheduled extended test remain available.
- A required pull-request status check can remain pending when GitHub skips a path-filtered workflow. If branch protection blocks a documentation-only PR, review the repository ruleset and use an appropriate documentation exemption or a manual check policy.

Changes to `docs/status-board.html`, `docs/index.html`, or `docs/assets/` do not publish automatically. Run the Pages workflow manually when the dashboard files are ready.

## App build and deployment

### Manual app workflow does not start

Run [app-deploy.yml](../.github/workflows/app-deploy.yml) from **Actions → Build, Test, and Deploy → Run workflow**. Select the intended Python version and provide an app-name override only when it differs from `AZURE_WEBAPP_NAME`.

### Azure deployment step is skipped

The deploy step is conditional on `AZURE_WEBAPP_NAME` being non-empty.

**Mitigation:** Add the `AZURE_WEBAPP_NAME` repository or environment secret, or supply the `app_name` workflow input. Confirm the workflow is allowed to read secrets from the selected environment.

### Azure rejects the publish profile

**Likely causes:** An expired or mismatched publish profile, a wrong Web App name, or a profile from another subscription.

**Mitigation:** Download a fresh publish profile from the target Azure Web App, update `AZURE_PUBLISH_PROFILE`, confirm `AZURE_WEBAPP_NAME`, and rerun the workflow.

### App deploy succeeds but the app is unhealthy

<img src="assets/tired-office.gif" width="560" alt="Tired Office"><br>Check runtime logs before repeating a deployment.

**Likely causes:** Missing runtime settings, incorrect Django working directory, missing dependencies, or Azure build configuration problems.

**Mitigation:** Check the Web App deployment log, confirm `requirements.txt` is included, verify the Python runtime, and run `python devtrack/manage.py check` locally before redeploying.

## Terraform app infrastructure

Run [azure-deploy.yml](../.github/workflows/azure-deploy.yml) manually with `plan` first and `apply` only after reviewing the plan.

### Terraform authentication fails

**Likely causes:** Missing `AZURE_SUBSCRIPTION_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, or `AZURE_CLIENT_SECRET`, expired service-principal credentials, or insufficient Azure role assignment.

**Mitigation:** Verify every secret in the selected GitHub environment and grant the service principal the required resource-group or subscription permissions.

### Terraform validation or provider initialization fails

**Likely causes:** An invalid HCL change, an unavailable provider version, a stale lock file, or a module source/path error.

**Mitigation:** Install Terraform 1.8.5 locally, then run:

```powershell
terraform fmt -recursive
terraform init
terraform validate
```

Run those commands from `infra/terraform` or `infra/terraform/runner`, depending on the workflow being tested.

### Terraform plan wants to replace resources unexpectedly

<img src="assets/eyebrow-raise-dwight.gif" width="560" alt="Careful review"><br>Pause and review the plan before applying it.

**Likely causes:** Renamed resources, changed names or locations, state drift, changed provider behavior, or a new module address.

**Mitigation:** Stop before apply. Review the complete plan, compare it with the intended change, inspect Azure for drift, and use state migration only when the resource identity really changed.

## Azure self-hosted runner

Run [runner-infra.yml](../.github/workflows/runner-infra.yml) manually before depending on the self-hosted runner.

### Runner provisioning fails before Terraform

**Likely causes:** Missing `GH_RUNNER_ADMIN_TOKEN` or insufficient permission to create a repository runner registration token.

**Mitigation:** Use a token that can manage Actions runners for this repository, store it as a GitHub secret, and never put it in Terraform files or static HTML.

### Runner VM does not appear online

**Likely causes:** Missing `AZURE_RUNNER_SSH_PUBLIC_KEY`, cloud-init failure, blocked outbound access, an invalid runner version, or an expired registration token.

**Mitigation:** Inspect Azure VM boot diagnostics, verify the SSH public key, confirm the VM can reach `github.com`, and rerun runner infrastructure to obtain a fresh short-lived registration token.

### App workflow cannot find a self-hosted runner

<img src="assets/office.gif" width="560" alt="Office team reaction"><br>The runner must be online before a self-hosted job can start.

**Likely causes:** The VM is offline, the runner service failed, or labels do not match `self-hosted`, `linux`, `azure`, and `devtrack`.

**Mitigation:** Check repository **Settings → Actions → Runners**, confirm the runner is online with the expected labels, and restart or reprovision the VM before rerunning app deployment.

## GitHub Pages status board

### Publisher fails at `configure-pages`

**Cause:** GitHub Pages has not been enabled for the repository, or its source is not set to GitHub Actions. The default `GITHUB_TOKEN` cannot create the Pages site.

**Mitigation:** Open **Settings → Pages**, select **GitHub Actions** as the source, save, and rerun [publish-status-board.yml](../.github/workflows/publish-status-board.yml).

### Publisher fails at artifact upload or deployment

**Likely causes:** Missing `docs/index.html`, missing `docs/status-board.html`, an invalid asset path, or Pages permissions/policy restrictions.

**Mitigation:** Confirm the files exist, validate all GIF paths, check that the workflow has `pages: write` and `id-token: write`, then rerun the workflow.

### Pages root returns 404

**Cause:** The published artifact does not contain `index.html` at its root.

**Mitigation:** Confirm [docs/index.html](index.html) exists and that the workflow uploads the entire `docs` directory. Republish the workflow, then wait briefly for Pages propagation.

### Dashboard loads but runs are stale

**Likely causes:** GitHub API rate limiting, a private repository without a secure proxy, browser caching, or an invalid repository/branch query parameter.

**Mitigation:** Refresh the page, verify the `owner/repository` and branch URL parameters, inspect browser developer tools, and wait for the 15-second polling cycle. When the public API quota is exceeded, rerun the Pages workflow so it refreshes the authenticated `status-board-data.json` snapshot. Never put a personal access token in the static board.

### Expanding a run shows no stage details

**Likely causes:** GitHub API rate limiting, a private repository without authenticated access, missing job permissions, or a workflow that has not created job step data yet.

**Mitigation:** Expand the run, click the individual stage to load its inline log, and use **Open the GitHub job log** if raw browser access is restricted. Confirm the repository is public or use a secure proxy, wait for an in-progress run to create job data, and inspect the browser developer tools for the jobs API response.

### Dashboard stops updating

<img src="assets/great-job.gif" width="560" alt="Great job"><br>Republish after confirming the dashboard files are ready.

**Mitigation:** Check the latest **Publish Pipeline Status Board** run in **Actions**. Use **Run workflow** after dashboard changes are ready to publish. If the run failed, fix the reported step and rerun it.

## Local verification checklist

Run this sequence from the repository root before pushing any Python, Django, API, test, or workflow-related code change.

### 1. Prepare the environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Revalidate all application code

```powershell
python -m compileall -q devtrack
python devtrack/manage.py check
python devtrack/manage.py test issues
```

Run the complete extended scenario set used by the extended pipeline:

```powershell
python devtrack/manage.py test issues.tests --verbosity 2
```

Check the API manually when a route or response changes:

```powershell
python devtrack/manage.py runserver
```

Then exercise the endpoints documented in [api.md](api.md), including valid requests, invalid JSON, duplicate IDs, missing reporters, status filters, and unsupported methods.

For Terraform code changes, run these commands from the affected Terraform root:

```powershell
terraform fmt -recursive
terraform init
terraform validate
terraform plan
```

Review the plan before any apply operation.

### 3. Revalidate the local pipeline dashboard

```powershell
python -m http.server 8000 --directory docs
```

Then verify:

- `http://127.0.0.1:8000/status-board.html`
- A branch URL with `&branch=main`
- A status URL with `&status=success`, `&status=running`, or `&status=failure`
- Every dashboard GIF loads
- Clicking a run expands its jobs and stages
- Clicking a stage loads its inline log or provides the GitHub job-log link
- The failed stage is identified when GitHub returns step data
