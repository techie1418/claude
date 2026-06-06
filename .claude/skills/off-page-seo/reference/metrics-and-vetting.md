# Metrics & Vetting — how to score DA / PA / Spam with the live tools

This is the engine behind "good DA/PA with low spam score." It maps the SEO concepts the
user cares about to the exact MCP tools available, gives thresholds, and defines the
ranking formula.

## Metric → tool map

| User-facing metric | What it really is | Tool to call | Notes |
|---|---|---|---|
| **DA (Domain Authority)** | SE Ranking **Domain InLink Rank** (0–100) | `DATA_getDomainAuthority` (single) or `DATA_getBacklinksSummary` with `target` as an **array** (batch) | SE Ranking's DA equivalent. Not Moz DA, but same 0–100 scale and purpose. |
| **PA (Page Authority)** | SE Ranking **InLink Rank** of a specific page (0–100) | `DATA_getPageAuthority` (target = the exact submission URL) or `DATA_getBacklinksAuthority` | Use for the page you'll actually get a link from. |
| **Spam score** | Likelihood the domain is spam (0–100% / 0–17) | **DataForSEO** Backlinks "Bulk Spam Score" | Needs DataForSEO auth (below). If unavailable, use the proxy below and label it. |
| Referring domains | Unique linking domains | `DATA_getBacklinksSummary` / `DATA_getTotalRefDomainsCount` | Volume + diversity signal. |
| Dofollow ratio | Share of followed links | `DATA_getBacklinksSummary` (dofollow/nofollow) | Natural profiles have a mix. |
| Anchor profile | Anchor text distribution | `DATA_getBacklinksAnchors` | Detect over-optimization. |
| Authority trend | DA over time | `DATA_getDomainAuthorityHistory` | Rising = healthy; crashing = risk. |
| Traffic / keywords | Organic strength | `DATA_getDomainOverviewByCountry`, `DATA_getDomainKeywords` | A "high DA" site with zero traffic is a red flag (link farm). |

### Batch vetting (do this — it's fast and quota-friendly)
`DATA_getBacklinksSummary` and `DATA_getBacklinksMetrics` accept an **array** of targets.
Pass up to a few dozen candidate domains in one call to get DA + referring domains + follow
split for all of them at once, then only spend single-call budget on the survivors.

## DataForSEO spam score setup
The `Data_For_SEO` MCP server exposes `authenticate` / `complete_authentication`. On first
use, call `mcp__Data_For_SEO__authenticate`, follow the returned flow, then
`mcp__Data_For_SEO__complete_authentication`. After that, its backlinks endpoints (incl.
**Bulk Spam Score** and **Backlinks Summary** with `backlinks_spam_score`) become callable —
search for them with ToolSearch (`select:` or keyword "spam score backlinks") once
authenticated. DataForSEO spam score is 0–100 (higher = spammier).

If the user hasn't authenticated DataForSEO and doesn't want to, **don't block** — compute
the proxy spam estimate and clearly label it `~estimated`.

### Proxy spam estimate (when DataForSEO spam score isn't available)
Flag a domain as higher-risk when several hold:
- DA is high but **referring domains are very few** or **organic traffic ≈ 0** (link farm pattern).
- **Dofollow ratio ~100%** with thousands of identical sitewide links.
- Anchor profile dominated by **exact-match commercial anchors** (`DATA_getBacklinksAnchors`).
- DA history is **volatile / spiking** (`DATA_getDomainAuthorityHistory`).
- Lots of links from **unrelated languages/topics**.
- The domain is a known free-for-all (auto-approve directory, comment farm).
Map to a 0–100 estimate and present as `~`. Never present the proxy as exact.

## Default quality thresholds (user can override at Step 3/6)
- **DA (Domain InLink Rank) ≥ 30** — raise to 40+ for competitive niches, lower to ~20 for
  fresh local directories that are still legitimately useful.
- **PA of the submission page ≥ 20**.
- **Spam score ≤ 1–2%** (DataForSEO) — the user asked for ~1%; treat ≤2% as the practical
  pass band and surface the exact number. Reject anything clearly toxic.
- **Live + indexable** — skip dead/deindexed sites.
- **Relevance** — topical or local match to the user's site (penalize generic/irrelevant).
- **Dofollow preferred**, but keep a natural follow/nofollow mix; nofollow from a giant
  brand (e.g. a major social profile) is still worth it.

## Opportunity score (sort the final table by this)
For each surviving candidate compute a 0–100 score:

```
score = 0.35 * DA_norm          # Domain InLink Rank / 100
      + 0.15 * PA_norm          # page InLink Rank / 100
      + 0.20 * spam_inverse     # (100 - spam_score) / 100
      + 0.15 * relevance        # 1.0 topical+local, 0.6 topical OR local, 0.2 generic
      + 0.10 * dofollow_bonus   # 1.0 dofollow, 0.5 nofollow
      + 0.05 * ease             # 1.0 free/instant, 0.5 needs outreach/approval, 0.2 paid
score = round(score * 100)
```
Sort descending. Group the table into "Do first" (score ≥ 65), "Worthwhile" (45–64),
"Optional / low priority" (< 45). Always show the raw DA/PA/Spam columns too, never just
the composite — the user explicitly wants to see DA/PA/spam.

## Vetting procedure (per run)
1. Assemble candidates (curated DB + competitor-link discovery).
2. De-duplicate to root domains.
3. **Batch** DA + referring-domain + follow data via `DATA_getBacklinksSummary([...])`.
4. Drop anything under the DA floor.
5. Spam-check survivors (DataForSEO bulk spam score, else proxy).
6. PA-check the specific submission pages for the top survivors (`DATA_getPageAuthority`).
7. Score, sort, group, present. Note any metric that is estimated.
