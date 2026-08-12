# Architecture

## Project structure

```
DevTrack/
├── devtrack/          # Django project package (settings, urls, wsgi)
├── issues/            # Django app
│   ├── models.py      # Data models
│   ├── views.py       # Request handling
│   ├── urls.py        # App-level routing
│   ├── reporters.json # Persisted reporter records
│   └── issues.json    # Persisted issue records
├── infra/terraform/   # Azure Web App Terraform root
│   ├── runner/        # Azure runner VM Terraform root
│   └── modules/       # Reusable Terraform modules
├── docs/              # This documentation folder
├── manage.py
└── requirements.txt
```

## Data model

Classes live in `issues/models.py`:

- `BaseEntity` — abstract base with `validate()` and `to_dict()`
- `Reporter(BaseEntity)` — validates reporter fields
- `Issue(BaseEntity)` — validates title, status, priority, and reporter reference
- `CriticalIssue(Issue)` — overrides `describe()` to prepend `[URGENT]`
- `LowPriorityIssue(Issue)` — overrides `describe()` for low-priority messaging

Model logic is kept separate from request handling in `views.py`.

## Data storage

JSON file persistence is used in place of a relational database:

- `issues/reporters.json`
- `issues/issues.json`

## Validation rules

### Reporter

- `name` must not be empty
- `email` must contain `@`

### Issue

- `title` must not be empty
- `status` must be one of: `open`, `in_progress`, `resolved`, `closed`
- `priority` must be one of: `low`, `medium`, `high`, `critical`
- `reporter_id` must be an integer referencing an existing reporter record
