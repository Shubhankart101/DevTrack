# Local pipeline status boards (inactive)

The pipeline board implementation is retained in `status-board.html` for future use but is currently inactive. It is not linked from the root README or served as the default Pages entrypoint. Running [publish-status-board.yml](../.github/workflows/publish-status-board.yml) replaces the published site with an inactive placeholder instead of publishing this board.

## Dashboard mood

Use the GIF cards in the dashboard as live status filters:

<img src="assets/office.gif" width="560" alt="Office team reaction"><br>**Failed runs** need investigation.

<img src="assets/bounce-dwight.gif" width="560" alt="Dwight bouncing"><br>**Running runs** are still in motion.

<img src="assets/great-job.gif" width="560" alt="Great job"><br>**Succeeded runs** are ready to celebrate.

The dashboard also includes reaction GIFs for code review, deployment celebration, unexpected results, debugging, and team reactions.

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
- Click any run to expand its job stages and identify the exact failed stage when GitHub exposes step data
- Counts for recent, running, passed, and failed runs
- Automatic refresh every 15 seconds

## Stop the local server

Return to the PowerShell terminal running the server and press `Ctrl+C`.

## Public repository limitation

The browser calls GitHub directly without exposing a token. This works for public repositories. GitHub API rate limits still apply. Do not put a personal access token in `status-board.html` or any other static file. For private repositories, use a secure server-side proxy or a GitHub Pages-compatible backend that stores the token as a secret.

## GitHub Pages

The board is published through the [publish-status-board workflow](../.github/workflows/publish-status-board.yml). Before the first publish, open **Repository Settings → Pages**, select **GitHub Actions** as the source, and save. The workflow cannot create the Pages site with the default repository token. After that one-time setup, start the publisher manually whenever the board or its GIF assets are ready. Use the published URL instead of the relative HTML source link:

```text
https://shubhankart101.github.io/DevTrack/status-board.html?repo=Shubhankart101%2FDevTrack&branch=main
```

## If the dashboard stops

The dashboard is a static Pages site. It does not run as a permanent local process or server; GitHub Pages serves the published files, while the browser polls GitHub Actions.

If the published dashboard stops updating:

1. Open the repository's **Actions** tab and inspect the latest **Publish Pipeline Status Board** run.
2. If the run failed at `configure-pages`, open **Settings → Pages** and set the source to **GitHub Actions**.
3. If the run failed during upload or deployment, rerun the failed workflow after checking the log.
4. If the site root returns 404, confirm that `docs/index.html` is included in the published artifact and rerun the workflow.
5. Check the GitHub Actions API response in the browser developer tools if the page loads but the run list is stale.

The publisher is manual-only. Start it after `docs/status-board.html`, `docs/index.html`, or `docs/assets/` changes are merged into `main` and ready to publish.
