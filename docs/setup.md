# Local development setup

## Prerequisites

- Python 3.11 or newer
- pip
- Optional: Git, virtualenv, PowerShell or Bash

## Steps

### 1. Clone and enter the repository

```bash
cd /path/to/DevTrack
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

### 4. Run startup checks

```bash
python manage.py check
```

### 5. Start the development server

```bash
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/`.

## Troubleshooting

1. Confirm Python and Django are installed in the active environment.
2. Run `python manage.py check` and review the output.
3. Ensure you are in the directory that contains `manage.py`.
