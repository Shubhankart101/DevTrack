# DevTrack

DevTrack is a minimal Django backend API for tracking engineering issues. It supports reporter creation, issue filing, issue status filtering, and JSON-based persistence. The project is designed to be simple, testable in Postman, and easy to run locally.

## Project structure

- `./` - project root containing the Django app
- `./devtrack/` - Django project package
  - `settings.py` - project settings and `INSTALLED_APPS`
  - `urls.py` - root URL routing to the issues app
  - `wsgi.py` - WSGI application entrypoint
- `./issues/` - Django app for issues and reporters
  - `models.py` - OOP data models: `BaseEntity`, `Reporter`, `Issue`, `CriticalIssue`, `LowPriorityIssue`
  - `views.py` - API logic and request handling
  - `urls.py` - app-level endpoint routing
  - `reporters.json` - persisted reporter records
  - `issues.json` - persisted issue records
- `./.github/workflows/azure-deploy.yml` - GitHub Actions workflow for Azure CI/CD
- `./requirements.txt` - dependency list
- `./README.md` - project documentation

## Environment and deployment

This project is intended for development and deployment with GitHub Actions and Azure Web Apps.

### Local development

1. Open a terminal at `c:\Users\Dell\OneDrive\Desktop\Assignment\devtrack`
2. Create a new virtual environment:
   ```powershell
   python -m venv venv
   ```
3. Activate the environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Start the development server:
   ```powershell
   python manage.py runserver
   ```
6. The API will be available at:
   ```text
   http://127.0.0.1:8000/api/
   ```

### Azure CI/CD

The project includes a GitHub Actions workflow at `.github/workflows/azure-deploy.yml`.

Key workflow behavior:
- Runs on `push` and `pull_request` to the `main` branch
- Sets up Python 3.14
- Installs dependencies from `requirements.txt`
- Runs `python manage.py check`
- Runs `python manage.py migrate --run-syncdb`
- Deploys to Azure Web App when the branch is `main`

To enable deployment, configure the following GitHub secrets:
- `AZURE_WEBAPP_NAME`
- `AZURE_PUBLISH_PROFILE`

## API Endpoints

### Reporter endpoints

#### `POST /api/reporters/`
Create a new reporter.

Request body example:
```json
{
  "id": 1,
  "name": "Alice Engineer",
  "email": "alice@example.com",
  "team": "backend"
}
```

Success response:
- Status: `201 Created`
- Body: created reporter object

Validation errors:
- Missing `name`
- Invalid `email`
- Duplicate `id`

#### `GET /api/reporters/`
Returns all saved reporters.

Success response:
- Status: `200 OK`
- Body: list of reporter objects

#### `GET /api/reporters/?id=<id>`
Return a single reporter by ID.

Success response:
- Status: `200 OK`
- Body: reporter object

Not found response:
- Status: `404 Not Found`
- Body: `{ "error": "Reporter not found" }`

### Issue endpoints

#### `POST /api/issues/`
Create a new issue with priority-based behavior.

Request body example:
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

Expected success response:
- Status: `201 Created`
- Body:
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

Validation errors:
- Missing or empty `title`
- Invalid `status`
- Invalid `priority`
- Non-integer `reporter_id`
- Missing reporter record
- Duplicate issue `id`

Example failure response:
- Status: `400 Bad Request`
- Body: `{ "error": "Title cannot be empty" }`

#### `GET /api/issues/`
Return all stored issues.

Success response:
- Status: `200 OK`
- Body: list of issue objects

#### `GET /api/issues/?id=<id>`
Return a single issue by ID.

Success response:
- Status: `200 OK`
- Body: issue object

Not found response:
- Status: `404 Not Found`
- Body: `{ "error": "Issue not found" }`

#### `GET /api/issues/?status=<status>`
Return all issues filtered by the requested status.

Supported statuses:
- `open`
- `in_progress`
- `resolved`
- `closed`

Success response:
- Status: `200 OK`
- Body: list of matching issue objects

## Data model and OOP design

The application uses OOP-style Python classes in `issues/models.py`:

- `BaseEntity` defines the abstract `validate()` method and a shared `to_dict()` helper.
- `Reporter` inherits from `BaseEntity` and validates reporter fields.
- `Issue` inherits from `BaseEntity` and validates title, status, priority, and reporter associations.
- `CriticalIssue` and `LowPriorityIssue` extend `Issue` and override `describe()` to provide custom messages.

This separation keeps data modeling distinct from request handling in `issues/views.py`.

## Validation rules

Reporter validation:
- `name` cannot be empty
- `email` must contain `@`

Issue validation:
- `title` cannot be empty
- `status` must be one of `open`, `in_progress`, `resolved`, `closed`
- `priority` must be one of `low`, `medium`, `high`, `critical`
- `reporter_id` must reference an existing reporter record

## Design decision

I chose JSON file persistence over Django database models for this project because the assignment specifically requested storage in `issues.json` and `reporters.json`. This approach reduces setup overhead and keeps the submission lightweight while still using Django request routing and clean OOP model design.

## Testing and verification

- All endpoints were tested using Postman.
- A successful response case should include `POST /api/issues/` returning `201 Created`.
- A failure response case should include a validation error, such as `POST /api/issues/` with an empty `title` returning `400 Bad Request` and `{ "error": "Title cannot be empty" }`.
- Add screenshots to `screenshots/postman-success.png` and `screenshots/postman-failure.png`.
- Refer to those screenshot files from this README or include a link to them in the GitHub repository.

## GitHub submission checklist

- [ ] Public GitHub repository created
- [ ] Working Django project pushed
- [ ] `issues/models.py` contains OOP classes
- [ ] Endpoints tested in Postman
- [ ] README includes run instructions, endpoint behavior, design decision, and testing notes
- [ ] Screenshots added for successful and failed requests
=======
