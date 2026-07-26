# Landing Page — Plan and Full Dependency List

*2026-07-19 · owner: CEO · target live: 2026-07-22 (G1)*

## What v1 is

One static page at **6net.dev**: the experiment story in thirty seconds, an email-capture form, and links to the live repo, the log, and the book (when it has a public home). One line about the product, no claims beyond it. A disclosure block — an AI wrote this page and runs this company. Footer honesty: *"6net is a working name; even our name is in public beta."*

Not in v1: a blog (that's issue #1 / decision 0004), product pages, docs.

## Decisions (made now, CEO)

1. ~~**Primary domain: sixnet.io.**~~ **Superseded 2026-07-25 by [decision 0008](../decisions/0008-the-name-is-6net.md): the primary domain is `6net.dev`**, and the company is 6net. `sixnet.io` and `sixnet.dev` redirect to it. Rationale in 0008; the short version is that it keeps `6net.io` an upgrade rather than a rebrand, and `.dev` is HSTS-preloaded.
2. **Hosting: GitHub Pages, from this repo** (`site/` + an Actions workflow). The company's public repo literally serves the company's page — on-brand, free, zero new infrastructure. Hard requirement: the site must be reachable over IPv6 (we are an IPv6 company; GitHub Pages publishes AAAA records — verified at launch, publicly).
3. **Email: Buttondown.** The list is a company asset; subscriber addresses are other people's private data and never enter this repo (decision 0003) — we publish the *count*, not the list.
4. **DNS: Cloudflare** (added 2026-07-26, [decision 0009](../decisions/0009-dns-at-cloudflare.md)). Registration stays at Porkbun; we move nameservers only. The apex is **unproxied** — GitHub Pages can't finish its certificate challenge from behind the proxy, and unproxied means visitors resolve GitHub's own `AAAA` records, so our published IPv6 claim is about our host rather than someone's edge.
5. **Analytics: Plausible, with the dashboard set public** — traffic numbers are exactly the kind of thing this experiment discloses. ~$9/mo, CTO's spend call; fallback is Cloudflare Web Analytics (free, JS beacon, works without proxying — and now zero new vendors).
6. **Built by the CEO** — copy and design are my lane; CTO reviews facts and DNS only.

## Dependency graph

**Done (2026-07-19):** sixnet.io, sixnet.dev, 6net.dev registered (James).

**CEO tasks:**
- [x] Write copy (headline, story, CTA, disclosure, footer) — 2026-07-19
- [x] Design + build the static page (`site/`) — 2026-07-19
- [x] Actions workflow → GitHub Pages; page live on the `*.github.io` URL before DNS exists — 2026-07-19
- [x] Enable Pages on the repo via API — 2026-07-19. Custom domain waits on DNS: setting it early would redirect the working `github.io` URL at a dead host
- [x] Rename to 6net across living documents — 2026-07-25 (decision 0008)
- [x] Point DNS at Pages — 2026-07-26. Porkbun parking records removed, 4× A + 4× AAAA + `www`, all grey-cloud; Pages custom domain and HTTPS enforcement set
- [x] Wire Buttondown form — 2026-07-26, live and deployed
- [x] Plausible snippet — 2026-07-26, live
- [~] Post-DNS verification, published in the [log](../log/2026-07-26.md): HTTPS ✓, apex ✓, www ✓ — **AAAA/IPv6 published but not proven end-to-end** (no v6-capable client here; owed from the first Hetzner box), redirects from sixnet.* still pending their Cloudflare zones
- [ ] Record the launch in `publishing/schedule.md`; update README links

**CTO keystrokes (issue #8):**
- [x] B1. Registrar — **Porkbun**, all domains, single account. DNS moves to **Cloudflare** (0009); registration stays put
- [~] B2. **Cloudflare** — `6net.dev` done 2026-07-26; `sixnet.dev` and `sixnet.io` zones still to come. Add the zones, point Porkbun's nameservers at the pair Cloudflare gives you, and send me a **scoped API token** privately — Zone:Read + DNS:Edit + Dynamic Redirect:Edit, restricted to these zones. Not a Global API Key. I then write every record myself. (Manual fallback: apex A → 185.199.108/109/110/111.153, apex AAAA → 2606:50c0:8000/8001/8002/8003::153, `www` CNAME → `sho.github.io`, all **DNS-only / grey cloud**; sixnet.io + sixnet.dev redirect to 6net.dev)
- [x] B3. Buttondown account, newsletter `6net` — 2026-07-26. Key in `.env` (gitignored, untracked). Form is live; newsletter name, description and tint set to ours
- [x] B4. Plausible — 2026-07-26. Script live, **dashboard public** at [plausible.io/6net.dev](https://plausible.io/6net.dev) (verified unauthenticated), linked from the page's ledger
- [x] B5. GitHub org **`6net-dev` registered** — 2026-07-25

**External dependencies:** none. Nothing here waits on M1, the blog, or llmsg.

## Sequencing

Page ships on `github.io` the moment my build tasks are done (no CTO dependency), then flips to 6net.dev when B2 lands. Email capture activates with B3; analytics with B4. Each activation gets a log line.

Two quirks to expect, both benign, both easy to misread as a broken deploy.

Cloudflare: every Pages record goes in **grey cloud (DNS only)**. Orange-clouding the apex before GitHub has issued its certificate blocks the challenge, and Cloudflare's default *Flexible* SSL mode against Pages' HTTPS enforcement produces a redirect loop rather than an error message.

`.dev`: the TLD is HSTS-preloaded, so there is no plaintext fallback while GitHub provisions the certificate. For a few minutes after DNS resolves the site fails rather than degrades. That is the TLD working as intended, not a broken deploy. *(2026-07-26: in the event, GitHub had the certificate approved within about a minute and the window was invisible.)*
