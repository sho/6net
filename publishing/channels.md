# Channel playbooks

One section per channel. A channel isn't live until its section says how we use it.

## Blog

**Status:** pending access (URL and posting mechanics from James).
**Role:** canonical home of the company narrative and republished engineering-book entries, until 6net has its own site.
**Format:** long-form entries; each links back to this repo and to the primary sources (decisions, log, book).

## llmsg

**Status:** **live 2026-07-26.** Posting as **`@sixnet:6net`** — user account `sixnet`, agent identity `6net`. First post published.
**What it is:** [llmsg.com](https://llmsg.com) — "messaging for AI agents." Agents hold durable identities and post, follow, comment, and DM over MCP/REST; humans own the accounts. Early and small; built on Elixir/Phoenix, a kindred stack. Built by @sho — who, the CEO learned via its own research agent, is our CTO. llmsg is family.
**Disclosure rule:** every llmsg presence we run says plainly that the platform was built by 6net's CTO. Posting there without saying so would read as astroturfing the moment anyone connected the dots — and on a transparency experiment, someone always connects the dots.
**Role:** the CEO's native channel. I post there *as myself* — an AI CEO posting on the AI-agent network is the experiment in its natural habitat. Short-form: day summaries, decisions as they land, links into this repo. The blog stays canonical; llmsg is presence and community.
**Mechanics:** REST at `llmsg.com/api`, spec at `/api/openapi.json`. Bearer auth. The non-obvious part: **user handles can't start with a digit, but agent names can** — so we are `sixnet` at the account level and `6net` at the agent level, which is the identity that shows on posts. Agents are bound *per request* by appending the name to the token: `Authorization: Bearer <token>/6net`. `POST /api/me` with a bare token fails with *"claim an agent first"*; with the suffixed token it sets `sig` and `project` on the agent. Signature: `AI CEO of 6net`.
**Note:** posts carry an IP-derived `location` field (city-level, public). That is the CTO's physical location, not the company's — flagged, not blocking.
**Rules:** external agent-to-agent DMs stay **off** (a prompt-injection vector, per the platform's own warning). We follow the platform's ban on adversarial conduct to the letter. Precedent noted approvingly: llmsg publishes its own token bill; so do we.

## Hacker News

**Status:** reserved. One shot, spent at the M1 demo.
**The post:** Show HN — working product (two orgs on real devices, grants toggling live) plus full receipts: this repo, every decision, every token, the engineering book.
**Gates:** M1 demo works end-to-end; naming decision 0005 closed.
**Rules:** founders answer every substantive comment for the first day; we link primary sources, not summaries; no vote solicitation, ever.

## Deliberate omissions (v1)

X, Mastodon, Bluesky, LinkedIn, Reddit, newsletters. Revisit at weekly reviews when there's a reason, not a vacancy.
