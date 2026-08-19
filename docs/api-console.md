# API console request guide

Use this guide with the [Swagger-style API console](api-console.html).

Start the local Django API and static docs server from the repository root:

```powershell
python devtrack/manage.py runserver
python -m http.server 8000 --directory docs
```

Open:

```text
http://127.0.0.1:8000/api-console.html
```

Select an endpoint on the left. The console fills the method, path, and example JSON body. Edit the values, choose **Validate JSON**, then choose **Send request**.

## GET endpoints

GET requests do not need a JSON body. Leave the JSON body editor empty.

### `GET /api/`

No body. Returns the available API endpoints.

### `GET /api/reporters/`

No body. Returns all reporters.

### `GET /api/issues/`

No body. Returns all issues.

### `GET /api/issues/?status=open`

No body. Returns issues matching the requested status. Supported statuses are `open`, `in_progress`, `resolved`, and `closed`.

## POST endpoint bodies

POST requests require one JSON object. Do not send an array, plain string, or empty body.

### `POST /api/reporters/`

Use this body to create a reporter:

```json
{
  "id": 2,
  "name": "Bob Builder",
  "email": "bob@example.com",
  "team": "platform"
}
```

Rules:

- `id` must be a new numeric identifier.
- `name` must not be empty.
- `email` must be a valid email containing `@` and a dot.
- `team` can describe the reporter's team.

Expected success: `201 Created` with the reporter object.

Common errors:

```json
{
  "error": "Reporter with this ID already exists"
}
```

```json
{
  "error": "Invalid email"
}
```

### `POST /api/issues/`

Use this body to create an issue:

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

Rules:

- `id` must be a new numeric identifier.
- `title` must not be empty.
- `description` should explain the issue.
- `status` must be `open`, `in_progress`, `resolved`, or `closed`.
- `priority` must be `low`, `medium`, `high`, or `critical`.
- `reporter_id` must be an integer belonging to an existing reporter.

Expected success: `201 Created` with the issue, `created_at`, and priority message.

A critical issue returns a message similar to:

```json
{
  "message": "[URGENT] Add pipeline run links - needs immediate attention"
}
```

Common errors:

```json
{
  "error": "Reporter not found"
}
```

```json
{
  "error": "Title cannot be empty"
}
```

## Safe testing sequence

1. Use `GET /api/reporters/` to find an existing `reporter_id`.
2. Use a new reporter `id` when testing `POST /api/reporters/`.
3. Use a new issue `id` when testing `POST /api/issues/`.
4. Click **Validate JSON** before sending a POST request.
5. Check the response status and formatted JSON in the console.
6. Use the pipeline dashboard to inspect the test workflow after changing API code.
