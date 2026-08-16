# DevTrack

DevTrack is a minimal Django backend API for tracking engineering issues. It supports reporter creation, issue filing, issue status filtering, and JSON-based persistence.

<p align="center">
	<img src="docs/assets/devtrack-code-loop.gif" width="560" alt="DevTrack code loop">
</p>

<p align="center"><a href=".github/workflows/terraform.yml">Reusable Terraform template</a></p>

<p align="center"><a href="https://shubhankart101.github.io/DevTrack/status-board.html?repo=Shubhankart101%2FDevTrack">Open the all-branches live status board</a> · <a href="https://shubhankart101.github.io/DevTrack/status-board.html?repo=Shubhankart101%2FDevTrack&branch=main">Open the main-branch live status board</a></p>

<p align="center"><sub>Start the status-board publisher manually after tracker or GIF changes merge into <code>main</code>.</sub></p>

## The DevTrack lifecycle

### 1. Pull request checks

<img src="docs/assets/office.gif" width="560" alt="Office team ready"><br>**<a href=".github/workflows/pull-request-tests.yml">Pull Request Tests</a>** keep every change honest.

### 2. Extended test run

<img src="docs/assets/bounce-dwight.gif" width="560" alt="Dwight bouncing"><br>**<a href=".github/workflows/extended-tests.yml">Extended Manual Tests</a>** get the test suite moving.

### 3. Build, test, and deploy

<img src="docs/assets/great-job.gif" width="560" alt="Great job"><br>**<a href=".github/workflows/app-deploy.yml">Build, Test, and Deploy</a>** when the checks pass.

### 4. Provision app infrastructure

<img src="docs/assets/thats-what-she-said-what-she-said.gif" width="560" alt="That's what she said"><br>**<a href=".github/workflows/azure-deploy.yml">Provision App Infrastructure</a>** before the API response writes itself.

### 5. Provision the runner

<img src="docs/assets/tired-office.gif" width="560" alt="Tired Office"><br>**<a href=".github/workflows/runner-infra.yml">Provision GitHub Runner Infrastructure</a>**, then debug, then repeat.

## Pipeline status board

### Queued

<img src="docs/assets/pipeline-queued.gif" width="560" alt="Pipeline queued"><br>Start with **<a href=".github/workflows/runner-infra.yml">Provision GitHub Runner Infrastructure</a>**.

### Running

<img src="docs/assets/pipeline-running.gif" width="560" alt="Pipeline running"><br>**<a href=".github/workflows/extended-tests.yml">Extended Manual Tests</a>** are executing.

### Passed

<img src="docs/assets/pipeline-success.gif" width="560" alt="Pipeline passed"><br>**<a href=".github/workflows/app-deploy.yml">Build, Test, and Deploy</a>** is ready to run.

Live boards: [all branches](docs/status-board.html?repo=Shubhankart101%2FDevTrack) · [main branch](docs/status-board.html?repo=Shubhankart101%2FDevTrack&branch=main) · [local setup guide](docs/status-board.md)

## Contents

| Section | Description |
| --- | --- |
| [Quick start](#quick-start) | Install dependencies, run checks, and start the API |
| [Application pipelines](#application-pipelines) | Review automatic, scheduled, manual, and pull-request workflows |
| [Documentation](#documentation) | Find the detailed setup, API, deployment, and architecture guides |

## Quick start

From the repository root:

```bash
python -m venv .venv
```

Activate the virtual environment, then install the dependencies:

```bash
pip install -r requirements.txt
```

Run the same checks used by application CI:

```bash
python devtrack/manage.py check
python devtrack/manage.py test issues
```

Start the development server with:

```bash
python devtrack/manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/`.

## Application pipelines

The repository has three application workflows:

| Workflow | Trigger | Purpose |
| --- | --- | --- |
| [Pull Request Tests](.github/workflows/pull-request-tests.yml) | Automatically on pull requests targeting `main` | Runs Django checks and the complete app test suite before merge |
| [Build, Test, and Deploy](.github/workflows/app-deploy.yml) | Manually from GitHub Actions | Compiles, checks, and tests the app, then optionally deploys it |
| [Extended Manual Tests](.github/workflows/extended-tests.yml) | Code-changing commits on every branch, Saturdays at 12:00 PM IST, or manually | Runs each API scenario as a separate sequential stage on a GitHub-hosted runner and prints dynamic results |

The `main` branch should require the pull-request test job as a branch protection status check and disallow direct pushes. Infrastructure workflows are documented separately in [docs/deployment.md](docs/deployment.md).

## Documentation

| Topic | File |
| --- | --- |
| Local setup & troubleshooting | [docs/setup.md](docs/setup.md) |
| API reference & examples | [docs/api.md](docs/api.md) |
| Deployment, pipelines & secrets | [docs/deployment.md](docs/deployment.md) |
| Pipeline troubleshooting & mitigation | [docs/README.md](docs/README.md) |
| Architecture, data model & validation | [docs/architecture.md](docs/architecture.md) |

## Until the next issue

<p align="center">
	<img src="docs/assets/tired-office.gif" width="560" alt="Tired Office debugging loop">
</p>





