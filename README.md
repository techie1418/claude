# Off-Page SEO AI Tool

An interactive AI assistant for **off-page SEO**, built as a [Claude Code skill](https://code.claude.com/docs).
You give it a website; it asks for your **target location** and **which off-page task** you
want to run, then uses live SEO data to return a **vetted, ranked list of real target
sites** (good DA/PA, low spam score) plus ready-to-paste submission and outreach content.

## Two ways to use it

**A) Local web app (visual, runs at `http://localhost:8000`):**

```bash
python3 web/server.py        # then open http://localhost:8000
```

No dependencies to install. Starts in demo mode; add DataForSEO keys to
`web/.env` for live DA/PA/spam data. See [`web/README.md`](web/README.md).

**B) Claude skill (full interactive flow inside Claude):**

In a Claude session with this repo, just say:

> run off-page SEO for `example.com`

or invoke the skill directly: `/off-page-seo`

It then walks you through:

1. **Target site** — confirms the domain.
2. **Location** — country/city you want to target (drives local directories + content language).
3. **Off-page task(s)** — pick from the full menu (multi-select):
   - Local SEO & citations
   - Link building (guest posts, niche edits, broken-link, **competitor backlink gap**, resource pages, HARO/digital PR)
   - Profile creation & Web 2.0
   - Social bookmarking
   - Content distribution (articles, PDF/doc, image, video, infographic, press release, podcast)
   - Forums, communities & Q&A
   - Classifieds & business listings
   - Reviews & reputation
   - Backlink audit / competitor analysis / toxic-link & disavow / link monitoring
4. **Vetted report** — a ranked table with **DA, PA, Spam %, type, dofollow, relevance,
   cost, difficulty**, grouped into do-first / worthwhile / optional.
5. **Content** — generates the actual bios, descriptions, anchor-text plan, outreach
   emails, etc. for the targets you choose.
6. **Tracking (optional)** — set up ongoing new/lost backlink monitoring.

## Where the data comes from

| Need | Source |
|---|---|
| Domain Authority (DA), Page Authority (PA), referring domains, backlink profile, competitor backlinks, anchors, keyword gaps | **SE Ranking** MCP server (connected) |
| Backlink **spam score** | **DataForSEO** MCP server (one-time auth; falls back to an estimated proxy if not authenticated) |
| Curated target-site database (directories, citations, Web 2.0, profiles, forums, etc.) | Bundled in the skill, **re-vetted live** before anything is recommended |

## What it does — and doesn't — do

✅ Researches, vets, prioritizes, and writes the content for an off-page campaign.
✅ Mines your competitors' backlinks for link opportunities you don't have yet.
✅ Filters every candidate by DA/PA/spam so you only work on quality sites.

❌ It does **not** auto-create accounts or auto-submit links on third-party sites — that
needs your own logins and usually breaks those sites' terms. You (or a VA) do the final
submit using the list + content it produces.
❌ White-hat only: no PBNs, bought spam links, or automated comment/forum spam.

## Project layout

```
.claude/skills/off-page-seo/
├── SKILL.md                       # the interactive workflow
└── reference/
    ├── off-page-tasks.md          # full task catalog (the task menu)
    ├── target-database.md         # curated high-DA, low-spam targets by category & region
    ├── metrics-and-vetting.md     # DA/PA/spam → tool mapping, thresholds, scoring formula
    └── templates.md               # submission & outreach content templates
```
