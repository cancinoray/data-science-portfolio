# Portfolio dashboard

A single Streamlit app that summarises all seven projects: headline metrics, two interactive charts
per project, a data snapshot, the key findings, the method, the caveat, and links back to the
notebook and README.

**Live app:** [data-science-portfolio-cancinoray.streamlit.app](https://data-science-portfolio-cancinoray.streamlit.app/)

![Portfolio dashboard](../assets/portfolio_dashboard.png)

## Run

From the repository root:

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

The theme lives in `.streamlit/config.toml` at the repo root, so run the command from the root (not
from inside `dashboard/`).

## What it reads

The dashboard **does not read the raw datasets**. It uses the results already produced by the
executed notebooks and committed with them. That makes it deployable without committing 150+ MB of
data, and it keeps the dashboard fast.

Each project page links to the full notebook for the method, diagnostics, and limitations. If you
change an analysis, update the corresponding metrics in `dashboard/app.py` and the notebook together.

## Structure

- `app.py` — page config, design tokens, project data, Altair charts, routing.
- Pages: Overview, plus 01–07.
- Per project: 4 KPI cards, a main chart, a supporting chart, 3 data-snapshot cards, findings,
  method, caveat, and links.
- Navigation: sidebar, project cards, and previous/next buttons.
- Links: notebook, project README, repository.

## Add a project

1. Add an entry to `PROJECTS` with metrics, findings, method, caveat, and links.
2. Add a `chart_*` function and register it in `CHARTS`.
3. `NAV_OPTIONS` and routing update automatically from `PROJECTS`.

## Deploy to Streamlit Community Cloud

1. Push this repository to GitHub with the dashboard committed.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Choose **New app**, then select:
   - Repository: `cancinoray/data-science-portfolio`
   - Branch: `main`
   - Main file path: `dashboard/app.py`
4. Click **Deploy**. No secrets, API keys, or data files are required.
5. Optionally set a custom subdomain in the app settings.

Streamlit installs the root `requirements.txt` automatically. It includes the notebook
dependencies as well, so the first build can take a couple of minutes. The app itself only imports
Streamlit, Altair, and pandas.

The theme config lives at the repo root (`.streamlit/config.toml`); Streamlit Cloud runs from the
repo root, so it is picked up automatically.
