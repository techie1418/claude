---
name: off-page-seo
description: Interactive off-page SEO assistant. Use when the user wants to run off-page SEO / link building for a website, find high-DA low-spam target sites (directories, citations, guest posts, profiles, Web 2.0, forums, content distribution, bookmarking, classifieds), analyze a competitor's backlinks for link opportunities, or generate submission/outreach content. Given a target site it asks for the location, asks which off-page task to run, then returns a vetted, ranked list of real target sites (good DA/PA, low spam) plus ready-to-use submission content.
---

# Off-Page SEO Assistant

This skill turns Claude into an end-to-end off-page SEO operator. The user gives a
site; Claude asks for the **target location** and the **off-page task**, then uses the
connected **SE Ranking** and **DataForSEO** MCP tools to vet a curated database of real
target sites and returns a ranked opportunity list with submission-ready content.

> **Be honest about scope.** This skill is the *brain* of an off-page campaign:
> research, vetting, prioritization, and content generation. It does **not** auto-submit
> to third-party sites or create accounts on the user's behalf — that needs the user's
> own logins/browser and often violates a site's terms. Deliver the vetted list +
> ready-to-paste content; the user (or a VA) does the final submit. Never fabricate
> backlinks, claim a link was placed, or invent metrics.

## The interactive flow

Run these steps in order. Ask one question at a time (use the AskUserQuestion tool when
offering choices). Do not skip the questions even if the user only pasted a URL.

### Step 1 — Capture the target site
Get the site URL/domain. Normalize to a root domain (e.g. `https://www.acme.com/` →
`acme.com`). Confirm it back to the user.

### Step 2 — Ask the target location
Ask which **country/city/region** they want to target. Map it to an SE Ranking regional
database code (the `source` param: `us`, `uk`, `de`, `fr`, `es`, `br`, `ca`, `au`, `in`,
`ae`, etc. — note SE Ranking uses `uk` not `gb`). Location drives:
- which **local citation / directory** sites apply (see `reference/target-database.md`),
- the `source` for competitor + keyword lookups,
- the language/region of generated submission content.

### Step 3 — Ask which off-page task(s) to run
Present the full task menu from `reference/off-page-tasks.md`. Let the user pick one or
several (multi-select). The menu covers **every** standard off-page tactic, grouped into:
1. Local SEO & citations
2. Link building (guest posts, niche edits, broken-link, competitor gap, resource pages, skyscraper, HARO)
3. Profile creation & Web 2.0
4. Social bookmarking
5. Content distribution (articles, PDF/doc sharing, image, video, infographic, press release, podcast)
6. Forums, communities & Q&A
7. Classifieds & business listings
8. Reviews & reputation
9. Analysis & monitoring (backlink audit, competitor backlink gap, toxic-link / disavow, link-velocity tracking)

### Step 4 — Establish a quality baseline for the user's own site
Before recommending targets, profile the user's site so recommendations are relevant and
you can detect a thin/spammy existing profile:
- `DATA_getBacklinksSummary` (target = root domain) → DA (Domain InLink Rank), referring domains, dofollow/nofollow split.
- `DATA_getDomainAuthority` → current DA.
- `DATA_getDomainCompetitors` (needs `source` from Step 2) → real competitors to mine for links.
- `DATA_getDomainKeywords` (top traffic keywords) → seed topics/anchors for guest posts & content.

### Step 5 — Build the candidate target list
Two sources, combined (this is the "curated DB + live vetting" model):
- **Curated database** — pull the task- and location-relevant sites from
  `reference/target-database.md`.
- **Live discovery** — for link-building tasks, mine competitor backlinks:
  - `DATA_getDomainCompetitors` → top 3–5 competitors.
  - `DATA_getBacklinksRefDomains` (per competitor, `order_by: domain_inlink_rank`) → their referring domains.
  - `DATA_getDomainKeywordsComparison` (`diff=1`) → keyword gaps to target with content.
  - Competitor referring domains the user's site does NOT have = link-gap opportunities.

### Step 6 — Vet every candidate (the DA/PA/spam filter)
This is the core promise: "good DA/PA with low spam score." For each candidate domain run
the vetting in `reference/metrics-and-vetting.md`. In short:
- **DA / Domain Authority** → `DATA_getDomainAuthority` or batch `DATA_getBacklinksSummary` (`target` accepts an array — vet many domains in one call).
- **PA / Page Authority** → `DATA_getPageAuthority` (for the specific submission URL/page).
- **Spam score** → DataForSEO `backlinks` "Bulk Spam Score" (needs DataForSEO auth — see vetting doc). If DataForSEO is unavailable, fall back to the SE Ranking proxy signals (referring-domain quality, dofollow ratio, edu/gov links, link-velocity sanity) and clearly label spam as "proxy/estimated."
- Apply thresholds (defaults; let the user override): **DA ≥ 30**, **PA ≥ 20** for the page, **spam score ≤ 1–2%**, live & indexable, topically/locally relevant, dofollow preferred (mix is healthy).

### Step 7 — Deliver the ranked report
Output a clean table sorted by an opportunity score (see vetting doc), plus a short action
plan. Always include these columns:

| # | Target site | Submit URL | DA | PA | Spam % | Type | Dofollow? | Relevance | Cost | Difficulty | Notes |

Then:
- Group by task type and by "do first / do later."
- Offer to export (write a CSV/Markdown file in the repo, or save to Google Drive via the
  `mcp__Google_Drive__create_file` tool if the user wants a shareable sheet).
- Offer to generate the **submission content** for the chosen targets using
  `reference/templates.md` (profile bios, business descriptions in multiple lengths,
  anchor-text plan, guest-post pitch emails, HARO responses, press release, classified ad
  copy, image/video metadata). Tailor anchors to the keywords found in Step 4 and keep the
  anchor mix natural (branded > naked URL > partial-match > exact-match).

### Step 8 — Track & follow up (optional)
Offer to set up ongoing tracking:
- Create an SE Ranking project (`PROJECT_createProject`) and add the target's keywords.
- Use `DATA_listNewLostReferringDomains` to watch new/lost links over time.
- Re-run vetting monthly; flag any newly-toxic referring domains for disavow.

## Anti-spam / safety rules (always enforce)
- Recommend **white-hat** tactics only. Refuse to build PBNs, buy spammy link packages,
  do automated mass blog-comment/forum spam, cloaking, or negative-SEO. If the user asks
  for these, explain the Google penalty risk and offer the white-hat alternative.
- Keep anchor text diversified and natural; warn against over-optimized exact-match anchors.
- Respect each platform's terms; submission is manual and user-driven.
- Never present estimated metrics as exact. Label any proxy/estimated spam score.

## Reference files
- `reference/off-page-tasks.md` — the complete off-page task catalog (the Step 3 menu) with what each is, when to use it, and the tools/templates it maps to.
- `reference/target-database.md` — curated high-DA, low-spam target sites by category and region, each tagged with approximate DA to verify live.
- `reference/metrics-and-vetting.md` — exactly which MCP tools to call, how DA/PA/spam map to them, DataForSEO spam-score setup, thresholds, and the opportunity-scoring formula.
- `reference/templates.md` — ready-to-use submission & outreach content templates.
