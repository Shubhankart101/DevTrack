# DevTrack

DevTrack is a minimal Django backend API for tracking engineering issues. It supports reporter creation, issue filing, issue status filtering, and JSON-based persistence.

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

The repository has two application workflows:

| Workflow | Trigger | Purpose |
| --- | --- | --- |
| [Pull Request Tests](.github/workflows/pull-request-tests.yml) | Automatically on pull requests targeting `master` | Runs Django checks and the complete app test suite before merge |
| [Build, Test, and Deploy](.github/workflows/app-deploy.yml) | Manually from GitHub Actions | Compiles, checks, and tests the app, then optionally deploys it |

The `master` branch should require the pull-request test job as a branch protection status check. Infrastructure workflows are documented separately in [docs/deployment.md](docs/deployment.md).

## Documentation

| Topic | File |
| --- | --- |
| Local setup & troubleshooting | [docs/setup.md](docs/setup.md) |
| API reference & examples | [docs/api.md](docs/api.md) |
| Deployment, pipelines & secrets | [docs/deployment.md](docs/deployment.md) |
| Architecture, data model & validation | [docs/architecture.md](docs/architecture.md) |




