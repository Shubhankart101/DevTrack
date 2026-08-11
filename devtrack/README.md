# DevTrack

DevTrack is a lightweight Django API for tracking engineering issues. It is designed for local development and rapid testing, with JSON-based persistence and a simple REST interface for managing reporters and issues.

## Overview

This project provides a small backend service for:
- creating reporters
- creating issues
- retrieving issues by ID or status
- persisting records in JSON files for easy local inspection

## Project structure

- [manage.py](manage.py) - Django entry point for the project
- [devtrack](devtrack) - Django project package and settings
- [issues](issues) - application logic, models, and API views
- [.github/workflows/azure-deploy.yml](.github/workflows/azure-deploy.yml) - CI/CD workflow for Azure deployment

## Local development setup

### Prerequisites

- Python 3.11 or newer
- pip
- Optional: Git, virtualenv, and PowerShell or Bash

### 1. Clone and enter the project

```bash
cd /path/to/devtrack
```

### 2. Create a virtual environment

Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run database and app initialization checks

```bash
python manage.py check
```

### 5. Start the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/api/
```

## API reference

### Reporter endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /api/reporters/ | Create a reporter |
| GET | /api/reporters/ | List all reporters |
| GET | /api/reporters/?id=<id> | Retrieve one reporter by ID |

### Issue endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /api/issues/ | Create an issue |
| GET | /api/issues/ | List all issues |
| GET | /api/issues/?id=<id> | Retrieve one issue by ID |
| GET | /api/issues/?status=<status> | Filter issues by status |

## Example requests

### Create an issue

```bash
curl -X POST http://127.0.0.1:8000/api/issues/ \
  -H "Content-Type: application/json" \
  -d '{"id":1,"title":"Login button not working","description":"Mobile issue","status":"open","priority":"critical","reporter_id":1}'
```

### Get all issues

```bash
curl http://127.0.0.1:8000/api/issues/
```

## Validation behavior

The API validates input for both reporters and issues.

### Reporter validation
- name must not be empty
- email must include an @ sign

### Issue validation
- title must not be empty
- status must be one of: open, in_progress, resolved, closed
- priority must be one of: low, medium, high, critical
- reporter_id must be an integer and reference an existing reporter

## Data storage

The project uses JSON files for persistence:
- [issues/reporters.json](issues/reporters.json)
- [issues/issues.json](issues/issues.json)

This is ideal for local development and lightweight demos.

## Azure deployment

A GitHub Actions workflow is included for deployment to Azure Web App using a Linux runner.

### Required repository secrets

Add these in GitHub repository settings:
- AZURE_WEBAPP_NAME
- AZURE_PUBLISH_PROFILE

### Deployment trigger

The workflow runs automatically on pushes to the main branch.

## Troubleshooting

If the app does not start:
1. Confirm Python and Django are installed in the active environment
2. Run `python manage.py check`
3. Ensure you are in the project directory that contains [manage.py](manage.py)
