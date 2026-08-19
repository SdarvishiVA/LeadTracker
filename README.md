# VA Capital — Lead Performance Dashboard

Automated pipeline: pulls each broker's Lead Log from Box, combines them,
and publishes a live performance statement for leadership.

## How it works

```
scripts/aggregate.py   -> reads broker files from Box, writes dashboard_data.json (repo root)
index.html             -> the dashboard, reads dashboard_data.json
.github/workflows/      -> runs aggregate.py once a day, commits the refreshed JSON
```

GitHub Pages serves the repo root as the public URL (Settings → Pages →
Source: Deploy from a branch → Branch: main → Folder: `/`). This keeps the
dashboard at the bare domain root, which matters once a custom domain is
pointed at it later. Every time the workflow runs
and the JSON changes, the live page updates automatically on next load —
no manual step required once this is fully wired up.

## Current status: DEMO MODE

This repo is running against two sample files (Suzana, Raph) bundled in
`scripts/sample_data/`, not live Box data. You'll see an amber "Demo mode"
banner on the site as a reminder. This lets everything else — the workflow,
the site, the styling — get proven out before the Box admin step happens.

## To go live

1. In Box Developer Console, create an app using **Client Credentials Grant
   (Server Authentication)**.
2. Have your Box admin authorize it in the Box Admin Console.
3. Share each broker's Lead Tracker folder with the app's Service Account
   (found on the app's Configuration tab).
4. In this repo: **Settings → Secrets and variables → Actions**, add:
   - `BOX_CLIENT_ID`
   - `BOX_CLIENT_SECRET`
   - `BOX_ENTERPRISE_ID`
5. That's it — the next scheduled run (or a manual run from the Actions
   tab) automatically switches from demo mode to live Box data. No code
   changes needed.

## Adding a broker

Open `scripts/aggregate.py`, add a line to the `BROKERS` list near the top:

```python
{"broker": "NewBrokerName", "box_file_id": "1234567890"},
```

The file ID is the number in the file's Box URL
(`https://app.box.com/file/`**`1234567890`**), or right-click the file in
Box → Share → Copy Shared Link, and pull the ID from there.

## Setting up GitHub Pages (one-time)

1. Repo **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: `main`, folder: **`/` (root)**
4. Save — GitHub gives you a URL like
   `https://<your-username>.github.io/<repo-name>/`

When you attach a custom domain later (Settings → Pages → Custom domain),
it'll point at this same root, so the dashboard loads directly at the
bare domain with no extra path.
