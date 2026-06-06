"""
Data layer for the Off-Page SEO tool.

Live data comes from DataForSEO's Backlinks API (domain rank, backlinks,
referring domains, and spam score). SE Ranking is supported as an optional
secondary token. Everything here is standard-library only (urllib) so the app
runs with just `python3` and no pip installs.

If no API credentials are configured the module returns deterministic DEMO data
so the UI works immediately; the response is clearly flagged mode="demo".
"""

import base64
import hashlib
import json
import os
import urllib.request
import urllib.error

DATAFORSEO_BASE = "https://api.dataforseo.com/v3"

# --------------------------------------------------------------------------
# Curated candidate database (compact mirror of
# .claude/skills/off-page-seo/reference/target-database.md). DA values here are
# only fallback hints for demo mode; live mode overwrites them with real data.
# Each entry: (domain, submit_url, type, dofollow, approx_da)
# --------------------------------------------------------------------------
GLOBAL = {
    "profiles": [
        ("about.me", "https://about.me", "Profile", True, 75),
        ("gravatar.com", "https://gravatar.com", "Profile", True, 92),
        ("crunchbase.com", "https://crunchbase.com", "Profile", True, 91),
        ("github.com", "https://github.com", "Profile", True, 96),
        ("behance.net", "https://behance.net", "Profile", True, 92),
        ("slideshare.net", "https://slideshare.net", "Profile", True, 95),
        ("medium.com", "https://medium.com", "Web 2.0 / Profile", True, 95),
        ("pinterest.com", "https://pinterest.com", "Profile", True, 94),
        ("producthunt.com", "https://producthunt.com", "Profile", True, 91),
    ],
    "web20": [
        ("wordpress.com", "https://wordpress.com", "Web 2.0", True, 94),
        ("blogger.com", "https://blogger.com", "Web 2.0", True, 99),
        ("tumblr.com", "https://tumblr.com", "Web 2.0", True, 86),
        ("substack.com", "https://substack.com", "Web 2.0", True, 90),
        ("medium.com", "https://medium.com", "Web 2.0", True, 95),
        ("weebly.com", "https://weebly.com", "Web 2.0", True, 93),
    ],
    "bookmarking": [
        ("reddit.com", "https://reddit.com", "Bookmarking", False, 94),
        ("mix.com", "https://mix.com", "Bookmarking", True, 81),
        ("pinterest.com", "https://pinterest.com", "Bookmarking", True, 94),
        ("flipboard.com", "https://flipboard.com", "Bookmarking", True, 92),
        ("diigo.com", "https://diigo.com", "Bookmarking", True, 90),
        ("scoop.it", "https://scoop.it", "Bookmarking", True, 89),
    ],
    "content": [
        ("issuu.com", "https://issuu.com", "Doc/PDF", True, 93),
        ("scribd.com", "https://scribd.com", "Doc/PDF", True, 94),
        ("slideshare.net", "https://slideshare.net", "Doc/PDF", True, 95),
        ("youtube.com", "https://youtube.com", "Video", True, 100),
        ("vimeo.com", "https://vimeo.com", "Video", True, 97),
        ("flickr.com", "https://flickr.com", "Image", True, 92),
        ("linkedin.com", "https://linkedin.com/pulse", "Article", True, 98),
    ],
    "qa_forums": [
        ("quora.com", "https://quora.com", "Q&A", False, 93),
        ("reddit.com", "https://reddit.com", "Community", False, 94),
        ("stackexchange.com", "https://stackexchange.com", "Q&A", True, 92),
        ("indiehackers.com", "https://indiehackers.com", "Community", True, 78),
    ],
    "citations": [
        ("business.google.com", "https://business.google.com", "Citation", False, 100),
        ("bing.com", "https://www.bing.com/maps", "Citation", False, 95),
        ("yelp.com", "https://biz.yelp.com", "Citation", False, 94),
        ("foursquare.com", "https://foursquare.com", "Citation", True, 93),
        ("yellowpages.com", "https://yellowpages.com", "Citation", True, 90),
        ("hotfrog.com", "https://hotfrog.com", "Citation", True, 80),
        ("manta.com", "https://manta.com", "Citation", True, 82),
        ("trustpilot.com", "https://trustpilot.com", "Review", True, 93),
    ],
    "classifieds": [
        ("craigslist.org", "https://craigslist.org", "Classified", False, 93),
        ("olx.com", "https://olx.com", "Classified", False, 88),
        ("locanto.com", "https://locanto.com", "Classified", True, 80),
        ("classifiedads.com", "https://classifiedads.com", "Classified", True, 72),
    ],
    "reviews": [
        ("trustpilot.com", "https://trustpilot.com", "Review", True, 93),
        ("g2.com", "https://g2.com", "Review", True, 91),
        ("capterra.com", "https://capterra.com", "Review", True, 91),
        ("glassdoor.com", "https://glassdoor.com", "Review", True, 92),
    ],
}

# Region-specific citation/classified additions, keyed by location code.
REGIONAL = {
    "in": [
        ("justdial.com", "https://justdial.com", "Citation", True, 84),
        ("sulekha.com", "https://sulekha.com", "Citation", True, 80),
        ("indiamart.com", "https://indiamart.com", "Citation", True, 87),
        ("quikr.com", "https://quikr.com", "Classified", False, 82),
    ],
    "uk": [
        ("yell.com", "https://yell.com", "Citation", True, 84),
        ("thomsonlocal.com", "https://thomsonlocal.com", "Citation", True, 70),
        ("freeindex.co.uk", "https://freeindex.co.uk", "Citation", True, 66),
        ("gumtree.com", "https://gumtree.com", "Classified", False, 84),
    ],
    "us": [
        ("angi.com", "https://angi.com", "Citation", True, 86),
        ("nextdoor.com", "https://nextdoor.com", "Citation", True, 90),
        ("superpages.com", "https://superpages.com", "Citation", True, 82),
        ("thumbtack.com", "https://thumbtack.com", "Citation", True, 86),
    ],
    "au": [
        ("yellowpages.com.au", "https://yellowpages.com.au", "Citation", True, 82),
        ("truelocal.com.au", "https://truelocal.com.au", "Citation", True, 72),
        ("startlocal.com.au", "https://startlocal.com.au", "Citation", True, 60),
    ],
    "ae": [
        ("yellowpages.ae", "https://yellowpages.ae", "Citation", True, 60),
        ("hidubai.com", "https://hidubai.com", "Citation", True, 62),
    ],
    "ca": [
        ("yellowpages.ca", "https://yellowpages.ca", "Citation", True, 84),
        ("n49.com", "https://n49.com", "Citation", True, 64),
    ],
    "de": [
        ("gelbeseiten.de", "https://gelbeseiten.de", "Citation", True, 80),
        ("meinestadt.de", "https://meinestadt.de", "Citation", True, 78),
    ],
}

# Map UI task ids -> curated DB buckets.
TASK_BUCKETS = {
    "local": ["citations"],
    "linkbuilding": ["content", "profiles"],  # plus live competitor discovery
    "profiles": ["profiles", "web20"],
    "bookmarking": ["bookmarking"],
    "content": ["content"],
    "forums": ["qa_forums"],
    "classifieds": ["classifieds"],
    "reviews": ["reviews"],
}

TASK_LABELS = {
    "local": "Local SEO & citations",
    "linkbuilding": "Link building",
    "profiles": "Profiles & Web 2.0",
    "bookmarking": "Social bookmarking",
    "content": "Content distribution",
    "forums": "Forums & Q&A",
    "classifieds": "Classifieds",
    "reviews": "Reviews & reputation",
}


# --------------------------------------------------------------------------
# Env loading (tiny .env parser, no dependency)
# --------------------------------------------------------------------------
def load_env(path=".env"):
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def have_dataforseo():
    return bool(os.environ.get("DATAFORSEO_LOGIN") and os.environ.get("DATAFORSEO_PASSWORD"))


# --------------------------------------------------------------------------
# DataForSEO REST client (urllib)
# --------------------------------------------------------------------------
def _dfs_post(path, payload):
    login = os.environ["DATAFORSEO_LOGIN"]
    pw = os.environ["DATAFORSEO_PASSWORD"]
    token = base64.b64encode(f"{login}:{pw}".encode()).decode()
    req = urllib.request.Request(
        DATAFORSEO_BASE + path,
        data=json.dumps(payload).encode(),
        headers={"Authorization": "Basic " + token, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def dfs_bulk_metrics(domains):
    """Return {domain: {da, spam, refdomains, backlinks}} using DataForSEO.

    Uses bulk_ranks (rank 0-1000 -> normalized to 0-100 DA) and
    bulk_spam_score (0-100). Falls back gracefully on partial failures.
    """
    out = {d: {} for d in domains}
    try:
        ranks = _dfs_post("/backlinks/bulk_ranks/live", [{"targets": domains}])
        for item in ranks["tasks"][0]["result"][0]["items"]:
            tgt = item["target"]
            # DataForSEO rank is 0-1000; normalize to a 0-100 DA-style score.
            out.setdefault(tgt, {})["da"] = round((item.get("rank") or 0) / 10)
            out[tgt]["backlinks"] = item.get("backlinks")
            out[tgt]["refdomains"] = item.get("referring_domains")
    except Exception as e:  # noqa: BLE001
        for d in domains:
            out[d]["error"] = f"ranks: {e}"
    try:
        spam = _dfs_post("/backlinks/bulk_spam_score/live", [{"targets": domains}])
        for item in spam["tasks"][0]["result"][0]["items"]:
            out.setdefault(item["target"], {})["spam"] = item.get("spam_score")
    except Exception as e:  # noqa: BLE001
        for d in domains:
            out[d].setdefault("error", f"spam: {e}")
    return out


# --------------------------------------------------------------------------
# Demo metrics (deterministic, no network) — used when no credentials
# --------------------------------------------------------------------------
def demo_metrics(domain, approx_da):
    h = int(hashlib.md5(domain.encode()).hexdigest(), 16)
    da = approx_da if approx_da else 30 + h % 60
    spam = h % 4  # 0-3%, mostly low for these curated high-trust sites
    refdomains = 1000 + (h % 90000)
    return {"da": da, "spam": spam, "refdomains": refdomains, "backlinks": refdomains * (3 + h % 9)}


# --------------------------------------------------------------------------
# Scoring (mirrors reference/metrics-and-vetting.md)
# --------------------------------------------------------------------------
def relevance_for(typ, has_location):
    if typ in ("Citation", "Classified", "Review"):
        return 1.0 if has_location else 0.6
    return 0.6


def opportunity_score(da, pa, spam, relevance, dofollow, ease):
    da_n = (da or 0) / 100
    pa_n = (pa or da or 0) / 100
    spam_inv = (100 - (spam or 0)) / 100
    do = 1.0 if dofollow else 0.5
    score = (0.35 * da_n + 0.15 * pa_n + 0.20 * spam_inv +
             0.15 * relevance + 0.10 * do + 0.05 * ease)
    return round(score * 100)


def ease_for(typ):
    if typ in ("Profile", "Web 2.0", "Bookmarking", "Doc/PDF", "Image", "Citation", "Classified"):
        return 1.0  # free / self-serve
    if typ in ("Q&A", "Community", "Review", "Article", "Video"):
        return 0.7  # needs quality content / moderation
    return 0.5      # outreach / guest post


def difficulty_label(ease):
    return {1.0: "Easy", 0.7: "Medium", 0.5: "Outreach"}.get(ease, "Medium")


# --------------------------------------------------------------------------
# Main analysis entry point
# --------------------------------------------------------------------------
def analyze(site, location, tasks, da_floor=30, spam_ceiling=2):
    location = (location or "us").lower()
    has_location = bool(location)

    # 1) assemble candidate pool from selected task buckets
    seen = set()
    candidates = []
    for task in tasks:
        for bucket in TASK_BUCKETS.get(task, []):
            for entry in GLOBAL.get(bucket, []):
                if entry[0] not in seen:
                    seen.add(entry[0])
                    candidates.append((task, *entry))
    # regional additions for local / classifieds / reviews tasks
    if any(t in ("local", "classifieds", "reviews") for t in tasks):
        for entry in REGIONAL.get(location, []):
            if entry[0] not in seen:
                seen.add(entry[0])
                candidates.append(("local", *entry))

    domains = [c[1] for c in candidates]

    # 2) metrics: live (DataForSEO) or demo
    mode = "demo"
    metrics = {}
    note = ""
    if have_dataforseo() and domains:
        mode = "live"
        metrics = dfs_bulk_metrics(domains)
        # if every domain errored, fall back to demo so the UI still works
        if all(metrics.get(d, {}).get("da") is None for d in domains):
            mode = "demo"
            note = "DataForSEO returned no data (check credentials / quota); showing demo metrics."

    # 3) build rows
    rows = []
    for task, domain, submit_url, typ, dofollow, approx_da in candidates:
        if mode == "live" and metrics.get(domain, {}).get("da") is not None:
            m = metrics[domain]
            da = m.get("da") or 0
            spam = m.get("spam")
            spam = 0 if spam is None else spam
            refdomains = m.get("refdomains")
        else:
            m = demo_metrics(domain, approx_da)
            da, spam, refdomains = m["da"], m["spam"], m["refdomains"]
        pa = max(da - 8, 0)  # page authority approx unless a specific URL is checked
        rel = relevance_for(typ, has_location)
        ease = ease_for(typ)
        score = opportunity_score(da, pa, spam, rel, dofollow, ease)
        passes = da >= da_floor and spam <= spam_ceiling
        rows.append({
            "task": TASK_LABELS.get(task, task),
            "site": domain,
            "submit_url": submit_url,
            "da": da, "pa": pa, "spam": spam,
            "refdomains": refdomains,
            "type": typ,
            "dofollow": dofollow,
            "relevance": round(rel, 1),
            "cost": "Free",
            "difficulty": difficulty_label(ease),
            "score": score,
            "passes": passes,
        })

    rows.sort(key=lambda r: r["score"], reverse=True)
    return {
        "site": site,
        "location": location,
        "tasks": [TASK_LABELS.get(t, t) for t in tasks],
        "mode": mode,
        "note": note,
        "da_floor": da_floor,
        "spam_ceiling": spam_ceiling,
        "count": len(rows),
        "passing": sum(1 for r in rows if r["passes"]),
        "rows": rows,
    }
