# Off-Page SEO Tool — local web app

A self-contained web UI for the off-page workflow: enter a **site**, choose a
**location** and **off-page task(s)**, and get a ranked, **DA / PA / spam-vetted**
list of target sites you can export to CSV.

**Standard-library only — no `pip install`, no build step.**

## Run it (on your own machine)

```bash
python3 web/server.py
```

Then open **http://localhost:8000**

That's it. It starts in **demo mode** so the UI works immediately with realistic
sample metrics.

## Turn on LIVE data (connect the API)

The live engine is **DataForSEO** (returns real domain rank → DA, referring
domains, and spam score). To connect it:

```bash
cp web/.env.example web/.env
# edit web/.env and set:
#   DATAFORSEO_LOGIN=...      (your DataForSEO API login)
#   DATAFORSEO_PASSWORD=...   (your DataForSEO API password)
python3 web/server.py
```

The badge in the header flips to **LIVE · DataForSEO** and every candidate is
vetted against real metrics. `web/.env` is git-ignored, so your keys never get
committed.

> Don't have a DataForSEO account? Get one at https://dataforseo.com (the
> Backlinks API covers bulk ranks + bulk spam score used here). SE Ranking is
> supported as an optional secondary token (`SERANKING_API_KEY`).

## How it works

```
web/
├── server.py        # stdlib HTTP server: serves the UI + /api/analyze
├── seo_clients.py   # curated target DB + DataForSEO REST client + scoring
├── static/index.html# the single-page UI (form → ranked results table → CSV export)
├── .env.example     # credentials template (copy to .env)
└── README.md
```

- **Candidate pool** = the curated high-DA / low-spam target database, filtered by
  your selected task(s) and location.
- **Vetting** = DataForSEO bulk ranks + bulk spam score (live) or deterministic
  demo metrics. Each candidate gets DA, PA (approx), Spam %, dofollow, relevance,
  difficulty, and a 0–100 opportunity score (same formula as the Claude skill's
  `reference/metrics-and-vetting.md`).
- **Filtering** = anything below your **Min DA** or above your **Max Spam %** is
  separated into a "filtered out" group so you only work on quality sites.

## Relationship to the Claude skill

This web app and the `.claude/skills/off-page-seo` skill share the same logic and
target database. Use the **web app** for a fast visual run + CSV export; use the
**skill** inside Claude for the full interactive flow including competitor
backlink-gap discovery and auto-generated submission/outreach content.

## Note about running it from a cloud/remote Claude session

If this repo is opened in a remote Claude environment, a `localhost` URL printed
there lives on the remote container and isn't reachable from your browser. Pull
the repo to your own machine and run the command above to use it locally.
