# API reference

Base URL: `http://127.0.0.1:8000/api/`

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
