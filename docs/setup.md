# Local development setup

![DevTrack code loop](assets/devtrack-code-loop.gif)

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

### 4. Run startup checks and tests

```bash
python devtrack/manage.py check
python devtrack/manage.py test issues
```

### 5. Start the development server

```bash
python devtrack/manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/`.

For live pipeline visibility, follow [status-board.md](status-board.md) to start the standalone board. Click a run to expand its stages, then click a stage to load its inline log or open the corresponding GitHub job log.

## Troubleshooting

1. Confirm Python and Django are installed in the active environment.
2. Run `python devtrack/manage.py check` and `python devtrack/manage.py test issues`.
3. Run management commands from the repository root, where the `devtrack` directory contains `manage.py`.
