# API reference

Base URL: `http://127.0.0.1:8000/api/`

## Interactive API console

Start the local static docs server with `python -m http.server 8000 --directory docs`, then open the [Swagger-style API console](api-console.html) at `http://127.0.0.1:8000/api-console.html`. It provides endpoint presets, editable JSON request bodies, a **Validate JSON** check before POST requests, response status codes, and formatted response output. See the [API console request guide](api-console.md) for the body schema of every endpoint.

## Reporter endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /api/reporters/ | Create a reporter |
| GET | /api/reporters/ | List all reporters |
| GET | /api/reporters/?id=\<id\> | Retrieve one reporter by ID |

### POST /api/reporters/

Request body:
```json
{
  "id": 1,
  "name": "Alice Engineer",
  "email": "alice@example.com",
  "team": "backend"
}
```

- `201 Created` — reporter created
- `400 Bad Request` — missing `name`, invalid `email`, or duplicate `id`
- `404 Not Found` — `{ "error": "Reporter not found" }` on GET by unknown ID

## Issue endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /api/issues/ | Create an issue |
| GET | /api/issues/ | List all issues |
| GET | /api/issues/?id=\<id\> | Retrieve one issue by ID |
| GET | /api/issues/?status=\<status\> | Filter issues by status |

### POST /api/issues/

Request body:
```json
{
  "id": 1,
  "title": "Login button not working on mobile",
  "description": "Users on iOS 17 cannot tap the login button",
  "status": "open",
  "priority": "critical",
  "reporter_id": 1
}
```

Response on success:
```json
{
  "id": 1,
  "title": "Login button not working on mobile",
  "description": "Users on iOS 17 cannot tap the login button",
  "status": "open",
  "priority": "critical",
  "reporter_id": 1,
  "created_at": "<timestamp>",
  "message": "[URGENT] Login button not working on mobile — needs immediate attention"
}
```

- `201 Created` — issue created
- `400 Bad Request` — validation failure (see [architecture.md](architecture.md#validation-rules))
- `404 Not Found` — `{ "error": "Issue not found" }` on GET by unknown ID

### Supported statuses

`open` · `in_progress` · `resolved` · `closed`

### Supported priorities

`low` · `medium` · `high` · `critical`

## Example curl requests

```bash
# Create a reporter
curl -X POST http://127.0.0.1:8000/api/reporters/ \
  -H "Content-Type: application/json" \
  -d '{"id":1,"name":"Alice Engineer","email":"alice@example.com","team":"backend"}'

# Create an issue
curl -X POST http://127.0.0.1:8000/api/issues/ \
  -H "Content-Type: application/json" \
  -d '{"id":1,"title":"Login button not working","description":"Mobile issue","status":"open","priority":"critical","reporter_id":1}'

# List all issues
curl http://127.0.0.1:8000/api/issues/

# Filter by status
curl http://127.0.0.1:8000/api/issues/?status=open
```

## Pipeline verification

After changing an endpoint, use the [live status board](status-board.md) to inspect the related workflow run. Expand the run, click an individual stage to load its inline log, and use the **Open the GitHub job log** link for complete output.

<img src="assets/great-job.gif" width="560" alt="Great job"><br>When the endpoint tests pass, the pipeline is ready to celebrate.
