# Local pipeline status boards

The pipeline boards are standalone HTML pages. They do not use Django, Terraform, or a local API server. The page calls the GitHub Actions API from the browser and refreshes every 15 seconds.

Automatic test workflows ignore commits that change only a `README.md` file. Code changes still trigger the workflows, and a commit containing both code and README changes also triggers them. Manual dispatch and scheduled runs are unaffected.

## Prerequisites

- Python 3.11 or newer
- Internet access
- A public GitHub repository, unless you add a secure proxy for private data

## Start the local board server

Open PowerShell at the repository root:

```powershell
python -m http.server 8000 --directory docs
```

Keep this terminal running. The `--directory docs` option makes the files in `docs/` available as a static site.

## Open the two boards

All branches:

```text
http://127.0.0.1:8000/status-board.html?repo=Shubhankart101%2FDevTrack
```

One branch, for example `main`:

```text
http://127.0.0.1:8000/status-board.html?repo=Shubhankart101%2FDevTrack&branch=main
```

Replace `main` with any branch name. The board preserves the selected repository and branch in the URL, so each branch has its own shareable local view:

```text
http://127.0.0.1:8000/status-board.html?repo=OWNER%2FREPOSITORY&branch=BRANCH_NAME
```

You can also change the repository and branch in the page controls and select **Refresh runs**. The URL updates automatically.

## Filter with the GIF controls

The entertaining GIF cards are live filters:

- Failed runs: `?status=failure`
- Running runs: `?status=running`
- Succeeded runs: `?status=success`

For example, the succeeded `main` view is:

```text
http://127.0.0.1:8000/status-board.html?repo=Shubhankart101%2FDevTrack&branch=main&status=success
```

Selecting a GIF updates the URL, so filtered boards can be bookmarked or shared locally.

## What the board shows

- Recent workflow runs from GitHub Actions
- Running, queued, passed, failed, and cancelled states
- Branch, actor, creation time, and a link to the GitHub run
- Run number and an explicit **Open GitHub run** link on every result
- Counts for recent, running, passed, and failed runs
- Automatic refresh every 15 seconds

## Stop the local server

Return to the PowerShell terminal running the server and press `Ctrl+C`.

## Public repository limitation

The browser calls GitHub directly without exposing a token. This works for public repositories. GitHub API rate limits still apply. Do not put a personal access token in `status-board.html` or any other static file. For private repositories, use a secure server-side proxy or a GitHub Pages-compatible backend that stores the token as a secret.

## GitHub Pages

The board is published through the [publish-status-board workflow](../.github/workflows/publish-status-board.yml). Before the first publish, open **Repository Settings → Pages**, select **GitHub Actions** as the source, and save. The workflow cannot create the Pages site with the default repository token. After that one-time setup, it publishes automatically when the board or its GIF assets merge into `main`, and it can also be run manually. Use the published URL instead of the relative HTML source link:

```text
https://shubhankart101.github.io/DevTrack/status-board.html?repo=Shubhankart101%2FDevTrack&branch=main
```
