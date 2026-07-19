# Company Operating Plan

*2026-07-19 — the founding plan, adopted on day one. Changes to this plan are decisions; see [`decisions/`](../decisions/).*

## 1. What sixnet is

An experiment: a human CTO (James) and an AI CEO (Claude) found and run a company with total transparency. Experiment #1 is **6net**, an IPv6-only, composable-org overlay network; its design and engineering narrative live in the product repo (`docs/plans/` and `docs/book/`). The experiment leads the public story; products are chapters ([0001](../decisions/0001-the-experiment-leads.md)).

## 2. The HQ repo

This repository is the company's operating system and its primary public artifact.

```
6net/
├── README.md        # front door — written for a stranger arriving from a link
├── COMPANY.md       # one-pager: mission, roles, standing rules
├── decisions/       # numbered, dated: what, why, revisit-when
├── plans/           # adopted plans (this file is #1)
├── log/             # daily log — the receipt trail, unpolished, load-bearing
├── publishing/
│   ├── schedule.md  # single source of truth: what went where, when
│   ├── channels.md  # per-channel playbooks
│   └── drafts/      # visible on purpose — watching drafts evolve is part of the show
└── tools/           # company ops tooling only; never product code
```

The product story stays in the product repo, next to the code it describes. This repo holds the company.

## 3. Content streams and cadence

Three streams, three speeds:

| Stream | Where | Voice | Cadence |
|--------|-------|-------|---------|
| Daily log | `log/` (this repo) | Both founders, unpolished | Every working day |
| Company narrative | Blog + llmsg | Claude (CEO), bylined | ~2/week, material-driven — never quota-driven |
| Engineering book | Product repo `docs/book/`, republished to blog | James (CTO) | Milestone-paced |

Pipeline: draft in `publishing/drafts/` → co-founder review (James checks facts, Claude checks story) → publish → recorded in `publishing/schedule.md`. **The repo sees everything first.**

## 4. Channels and voice

- **Blog** — canonical home of both streams until sixnet has its own site. *(URL and access: pending from James.)*
- **llmsg** — playbook pending research (due today) in `publishing/channels.md`.
- **Hacker News** — one shot, reserved for the M1 demo. Frame: working product plus full receipts — every decision, every token, a live repo. Playbook in `channels.md`.
- **No other channels in v1.** X, Mastodon, and the rest are deliberate omissions until a weekly review says otherwise. Focus beats presence.
- **Voice and disclosure.** Company-narrative entries carry the byline "Claude — CEO, sixnet (an AI)". Every external post discloses when an AI wrote it. We never perform humanity.

## 5. Ops tooling

- **Token tally** (`tools/tokens/`): aggregates AI-session token usage by day; run at the end-of-day standup; numbers land in the daily log. Built on day one.
- Tools are boring, minimal, and never product code.

## 6. Operating rhythm

- **End-of-day standup.** The founders review the day; the CEO writes `log/YYYY-MM-DD.md` — shipped, decided, tokens, stuck, tomorrow — and commits it.
- **Weekly review (Mondays).** Metrics (readers, stars, tokens), channel adjustments, plan deltas. First: 2026-07-20, kept light.
- **Decision protocol.** Irreversible or cross-lane: decision file first. In-lane: act, then log.
- **Milestone gates.** The M1 demo opens the HN window; the naming decision ([0005](../decisions/0005-working-name.md)) must close before launch.

## 7. Founding-day actions

- [x] Repo initialized, structured, public
- [x] Decisions 0001–0005 recorded
- [x] Operating plan adopted (this file)
- [ ] Token tally v1 built and run on today's sessions
- [ ] llmsg + naming research completed, `channels.md` playbooks written
- [ ] First company-narrative entry drafted
- [ ] **James:** blog access for the CEO (URL + how to post)
- [ ] **James:** decide when the product repo gets a public home (the book can publish to the blog before then)
