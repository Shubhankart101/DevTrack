# DevTrack

DevTrack is a minimal Django backend API for tracking engineering issues. It supports reporter creation, issue filing, issue status filtering, and JSON-based persistence.

<p align="center">
	<img src="docs/assets/devtrack-code-loop.gif" width="560" alt="DevTrack code loop">
</p>

<p align="center"><a href=".github/workflows/terraform.yml">Reusable Terraform template</a></p>

<p align="center"><a href="https://shubhankart101.github.io/DevTrack/status-board.html?repo=Shubhankart101%2FDevTrack">Open the live pipeline runs dashboard</a></p>

<p align="center"><a href="https://github.com/Shubhankart101/DevTrack/actions">Open the active pipeline runs dashboard</a></p>

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

Use the local [Swagger-style API console](docs/api-console.html) at `http://127.0.0.1:8000/api-console.html` to select endpoints, edit JSON request bodies, validate them, send requests, and inspect responses.

## API console examples

Start Django and the docs server first:

```powershell
python devtrack/manage.py runserver
python -m http.server 8000 --directory docs
```

Open `http://127.0.0.1:8000/api-console.html`, select an endpoint, copy the request values below, and choose **Send request**.

### 1. API root

**Request**

```text
GET http://127.0.0.1:8000/api/
```

**Response: `200 OK`**

```json
{
	"endpoints": [
		"/api/reporters/",
		"/api/reporters/?id=<id>",
		"/api/issues/",
		"/api/issues/?id=<id>",
		"/api/issues/?status=<status>"
	]
}
```

### 2. List reporters

**Request**

```text
GET http://127.0.0.1:8000/api/reporters/
```

**Response: `200 OK`**

```json
[
	{
		"id": 1,
		"name": "Alice Engineer",
		"email": "alice@example.com",
		"team": "backend"
	}
]
```

### 3. Get one reporter

**Request**

```text
GET http://127.0.0.1:8000/api/reporters/?id=1
```

**Response: `200 OK`**

```json
{
	"id": 1,
	"name": "Alice Engineer",
	"email": "alice@example.com",
	"team": "backend"
}
```

**Missing reporter response: `404 Not Found`**

```json
{
	"error": "Reporter not found"
}
```

### 4. Create a reporter

**Request**

```http
POST http://127.0.0.1:8000/api/reporters/
Content-Type: application/json
```

```json
{
	"id": 2,
	"name": "Bob Builder",
	"email": "bob@example.com",
	"team": "platform"
}
```

**Response: `201 Created`**

```json
{
	"id": 2,
	"name": "Bob Builder",
	"email": "bob@example.com",
	"team": "platform"
}
```

**Invalid reporter response: `400 Bad Request`**

```json
{
	"error": "Invalid email"
}
```

### 5. List issues

**Request**

```text
GET http://127.0.0.1:8000/api/issues/
```

**Response: `200 OK`**

```json
[
	{
		"id": 1,
		"title": "Login button not working",
		"description": "Mobile issue",
		"status": "open",
		"priority": "critical",
		"reporter_id": 1,
		"created_at": "<timestamp>",
		"message": "[URGENT] Login button not working - needs immediate attention"
	}
]
```

### 6. Get one issue

**Request**

```text
GET http://127.0.0.1:8000/api/issues/?id=1
```

**Response: `200 OK`**

```json
{
	"id": 1,
	"title": "Login button not working",
	"description": "Mobile issue",
	"status": "open",
	"priority": "critical",
	"reporter_id": 1,
	"created_at": "<timestamp>",
	"message": "[URGENT] Login button not working - needs immediate attention"
}
```

**Missing issue response: `404 Not Found`**

```json
{
	"error": "Issue not found"
}
```

### 7. Filter issues by status

**Request**

```text
GET http://127.0.0.1:8000/api/issues/?status=open
```

**Response: `200 OK`**

```json
[
	{
		"id": 1,
		"title": "Login button not working",
		"description": "Mobile issue",
		"status": "open",
		"priority": "critical",
		"reporter_id": 1,
		"created_at": "<timestamp>",
		"message": "[URGENT] Login button not working - needs immediate attention"
	}
]
```

Supported statuses are `open`, `in_progress`, `resolved`, and `closed`.

### 8. Create an issue

**Request**

```http
POST http://127.0.0.1:8000/api/issues/
Content-Type: application/json
```

```json
{
	"id": 2,
	"title": "Add pipeline run links",
	"description": "Show the relevant GitHub Actions run from the dashboard.",
	"status": "open",
	"priority": "high",
	"reporter_id": 1
}
```

**Response: `201 Created`**

```json
{
	"id": 2,
	"title": "Add pipeline run links",
	"description": "Show the relevant GitHub Actions run from the dashboard.",
	"status": "open",
	"priority": "high",
	"reporter_id": 1,
	"created_at": "<timestamp>",
	"message": "Add pipeline run links [high]"
}
```

**Validation failure response: `400 Bad Request`**

```json
{
	"error": "Title cannot be empty"
}
```

Use a new numeric `id` for each POST example because duplicate IDs are rejected.

## Application pipelines

The repository has three application workflows:

| Workflow | Trigger | Purpose |
| --- | --- | --- |
| [Pull Request Tests](.github/workflows/pull-request-tests.yml) | Automatically on pull requests targeting `main` | Runs Django checks and the complete app test suite before merge |
| [Build, Test, and Deploy](.github/workflows/app-deploy.yml) | Manually from GitHub Actions | Compiles, checks, and tests the app, then optionally deploys it |
| [Extended Manual Tests](.github/workflows/extended-tests.yml) | Code-changing commits on every branch, Saturdays at 12:00 PM IST, or manually | Runs each API scenario as a separate sequential stage on a GitHub-hosted runner and prints dynamic results |

The `main` branch should require the pull-request test job as a branch protection status check and disallow direct pushes. Infrastructure workflows are documented separately in [docs/deployment.md](docs/deployment.md).

Use the [pipeline troubleshooting guide](docs/README.md) when a run is skipped or fails. The live-run tracker dashboard is available through GitHub Pages.

Click a pipeline run to expand it, then click an individual stage to view its inline log or open the full GitHub job log.

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





