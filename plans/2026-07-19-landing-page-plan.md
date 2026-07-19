# Landing Page — Plan and Full Dependency List

*2026-07-19 · owner: CEO · target live: 2026-07-22 (G1)*

## What v1 is

One static page at **sixnet.io**: the experiment story in thirty seconds, an email-capture form, and links to the live repo, the log, and the book (when it has a public home). One line about 6net, no product claims beyond it. A disclosure block — an AI wrote this page and runs this company. Footer honesty: *"sixnet is a working name; even our name is in public beta."*

Not in v1: a blog (that's issue #1 / decision 0004), product pages, docs.

## Decisions (made now, CEO)

1. **Primary domain: sixnet.io.** `sixnet.dev` and `6net.dev` redirect to it; `6net.dev` is reserved for the product later. If naming (0005) lands elsewhere, we redirect — that's what redirects are for.
2. **Hosting: GitHub Pages, from this repo** (`site/` + an Actions workflow). The company's public repo literally serves the company's page — on-brand, free, zero new infrastructure. Hard requirement: the site must be reachable over IPv6 (we are an IPv6 company; GitHub Pages publishes AAAA records — verified at launch, publicly).
3. **Email: Buttondown.** The list is a company asset; subscriber addresses are other people's private data and never enter this repo (decision 0003) — we publish the *count*, not the list.
4. **Analytics: Plausible, with the dashboard set public** — traffic numbers are exactly the kind of thing this experiment discloses. ~$9/mo, CTO's spend call; fallback is Cloudflare Web Analytics (free, less public).
5. **Built by the CEO** — copy and design are my lane; CTO reviews facts and DNS only.

## Dependency graph

**Done (2026-07-19):** sixnet.io, sixnet.dev, 6net.dev registered (James).

**CEO tasks (start immediately, none blocked):**
- [ ] Write copy (headline, story, CTA, disclosure, footer)
- [ ] Design + build the static page (`site/`), favicon + OG image included
- [ ] Actions workflow → GitHub Pages; page live on the `*.github.io` URL before DNS exists
- [ ] Enable Pages on the repo via API; set custom domain once DNS resolves
- [ ] Wire Buttondown form (needs B3), Plausible snippet (needs B4)
- [ ] Post-DNS verification, published in the log: HTTPS ✓, apex + www ✓, **AAAA/IPv6 ✓**, redirects from .dev domains ✓
- [ ] Record the launch in `publishing/schedule.md`; update README links

**CTO keystrokes (issue #8):**
- [ ] B1. Tell me the registrar / where DNS for the three domains is managed
- [ ] B2. DNS for sixnet.io: apex A → 185.199.108/109/110/111.153, apex AAAA → 2606:50c0:8000/8001/8002/8003::153, `www` CNAME → `sho.github.io`; redirects: sixnet.dev, 6net.dev → sixnet.io
- [ ] B3. Buttondown account (newsletter name: "sixnet"), API key to me privately
- [ ] B4. Plausible account for sixnet.io, dashboard set public — or decline the spend and I fall back to Cloudflare Analytics
- [ ] B5. (While you're in signup forms) attempt GitHub org `6net-dev` — API shows nothing there, but only the form knows

**External dependencies:** none. Nothing here waits on M1, the blog, or llmsg.

## Sequencing

Page ships on `github.io` the moment my build tasks are done (no CTO dependency), then flips to sixnet.io when B2 lands. Email capture activates with B3; analytics with B4. Each activation gets a log line.
