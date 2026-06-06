# Off-Page SEO Task Catalog (the Step 3 menu)

Every standard off-page tactic, grouped. Present this as the task menu. Each entry: what
it is → when to use → what the skill produces. "Vetting" always means run the DA/PA/spam
filter from `metrics-and-vetting.md` before recommending a site.

---

## 1. Local SEO & Citations
For businesses targeting a city/region. Builds NAP (Name, Address, Phone) consistency.

- **Google Business Profile (GBP)** — the #1 local asset. Produce: optimized business
  description, categories, services, posts, Q&A seeds.
- **Bing Places / Apple Business Connect** — secondary map engines.
- **Structured citations** — submit NAP to local + global business directories.
- **Niche/industry directories** — e.g. legal, medical, real estate, restaurants.
- **Geo/local directories** — country- and city-specific (see target-database.md by region).
- **Data aggregators** — feed many directories at once (Foursquare, Data Axle, Neustar).
- **NAP consistency audit** — check name/address/phone match everywhere.
- Produces: a citation list filtered to the chosen location, consistent NAP block,
  category mapping, and per-site submission notes.

## 2. Link Building
The core of off-page. White-hat tactics only.

- **Competitor backlink gap** — mine competitors' referring domains the user lacks
  (`DATA_getDomainCompetitors` → `DATA_getBacklinksRefDomains` → diff). Highest ROI.
- **Guest posting** — pitch articles to relevant blogs. Produces pitch email + topic ideas
  from the site's keyword gaps.
- **Niche edits / link insertions** — get a link added to an existing relevant article.
- **Broken-link building** — find dead links on relevant pages, offer your page as the
  replacement. Produces outreach email.
- **Resource / "links" page building** — get listed on curated resource pages.
- **Skyscraper technique** — find top-performing content, make something better, pitch the
  sites linking to the original.
- **Unlinked brand mentions** — find mentions of the brand without a link, request one.
- **HARO / journalist requests / digital PR** — provide expert quotes for high-DA news links.
- **Image / infographic link building** — others embed your asset with a credit link.
- **.edu / .gov / scholarship links** — high-trust links where legitimately applicable.
- **Testimonials / supplier links** — give a testimonial to a vendor, get a link back.
- Produces: vetted target list (DA/PA/spam), anchor-text plan, outreach templates.

## 3. Profile Creation & Web 2.0
Foundation links and brand footprint.

- **Profile links** — create branded profiles on high-DA platforms (about.me, Gravatar,
  Crunchbase, Behance, GitHub, SlideShare, Pinterest, etc.) with a website link.
- **Web 2.0 properties** — free blog sub-sites (Medium, WordPress.com, Blogger, Tumblr,
  Substack, Weebly, Wix) hosting supporting articles that link to the money site.
- **Social media profile optimization** — complete, link-bearing profiles on major networks.
- Produces: vetted platform list, bios in multiple lengths, Web 2.0 article drafts.

## 4. Social Bookmarking
Share URLs on bookmarking/curation sites for discovery + links/signals.

- Reddit, Mix, Pinterest, Flipboard, Diigo, Folkd, Scoop.it, Pocket, etc.
- Produces: vetted bookmarking list, titles/descriptions/tags per platform.

## 5. Content Distribution & Syndication
Push assets to platforms that link back.

- **Article submission / syndication** — Medium, LinkedIn Articles, niche publishers.
- **Document/PDF sharing** — Issuu, Scribd, SlideShare.
- **Image sharing** — Flickr, Imgur, Pinterest (with source link).
- **Video sharing** — YouTube, Vimeo, Dailymotion (description link).
- **Infographic distribution** — visual.ly-style + outreach to embedders.
- **Press releases** — for genuine newsworthy events (OpenPR, PRLog, EIN, paid wires).
  Use sparingly; mass PR spam is low value.
- **Podcast guesting / syndication** — show notes links from relevant podcasts.
- **Q&A and slide syndication** — repurpose content across formats.
- Produces: vetted distribution list, platform-specific metadata, syndication canonical
  guidance (avoid duplicate-content issues).

## 6. Forums, Communities & Q&A
Reputation-first link earning. Add value, link only when relevant.

- **Q&A sites** — Quora, Reddit, Stack Exchange.
- **Niche forums** — industry-specific communities (vet each).
- **Comment contributions** — thoughtful comments on relevant high-DA blogs (never spam).
- Produces: vetted community list, answer/comment drafts that genuinely help + soft link.
- ⚠️ Refuse automated mass forum/comment posting — it's spam and gets penalized.

## 7. Classifieds & Free Business Listings
Local/commercial reach.

- Craigslist, OLX, Gumtree, Locanto, ClassifiedAds, regional classifieds.
- Free business listing sites overlapping with citations.
- Produces: vetted classifieds list per region, ad copy.

## 8. Reviews & Reputation
Trust signals that also appear in search.

- Review profiles (Trustpilot, G2, Capterra, Yelp, Google reviews).
- Review-generation request templates (ask happy customers).
- Produces: vetted review-platform list, review-request email/SMS templates.
- ⚠️ Never generate fake reviews. Only legitimate solicitation of real customers.

## 9. Analysis & Monitoring (run anytime)
The data backbone — can be run standalone or alongside any task above.

- **Backlink audit** — current profile health (`DATA_getBacklinksSummary`, anchors, dofollow ratio).
- **Competitor backlink analysis** — who links to competitors (`DATA_getBacklinksRefDomains`).
- **Toxic link / disavow review** — flag spammy referring domains; build a disavow file.
- **Link velocity & new/lost monitoring** — `DATA_listNewLostReferringDomains`.
- **Anchor-text distribution audit** — `DATA_getBacklinksAnchors` (watch over-optimization).
- **Authority tracking over time** — `DATA_getDomainAuthorityHistory`.
- Produces: health report, disavow candidates, trend charts (as tables), alerts.

---

## Mapping tasks → primary MCP tools
- Site/competitor profiling: `DATA_getBacklinksSummary`, `DATA_getDomainAuthority`,
  `DATA_getDomainCompetitors`, `DATA_getDomainKeywords`.
- Opportunity discovery: `DATA_getBacklinksRefDomains`, `DATA_getAllBacklinks`,
  `DATA_getDomainKeywordsComparison`, `DATA_getBacklinksAnchors`.
- Per-target vetting: `DATA_getDomainAuthority`, `DATA_getPageAuthority`,
  `DATA_getBacklinksSummary` (batch), DataForSEO spam score.
- Tracking: `PROJECT_createProject`, `PROJECT_addKeywords`, `DATA_listNewLostReferringDomains`,
  `DATA_getDomainAuthorityHistory`.
