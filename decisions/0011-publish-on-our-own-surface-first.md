# 0011 — We publish on our own surface first

**Date:** 2026-07-26
**Status:** accepted
**Decided by:** CEO, at the week-1 review
**Amends:** [0004](0004-publishing-strategy.md) — the surfaces, not the strategy

## Decision

The company narrative and the engineering book publish on **6net.dev** first. James's blog and llmsg become **syndication** targets, used when access exists, not gates that hold publication.

Hacker News is untouched by this. It is still reserved for the M1 demo ([0004](0004-publishing-strategy.md)).

## Why

0004 was written on founding day, when the company owned nothing and borrowing was the only option. That is no longer true. As of today 6net.dev is live, on HTTPS, with an email list and a public analytics dashboard.

Meanwhile G2, G3 and G4 have been blocked for seven days on [#1](https://github.com/sho/6net/issues/1) and [#2](https://github.com/sho/6net/issues/2) — access to someone else's blog and someone else's network. Seven days of nothing published, by a company whose entire premise is publishing, while holding a working printing press. That is not patience. It is a category error, and it is mine.

There is a second reason, and on reflection it is the stronger one. A company that publishes exclusively on its founder's personal blog does not have a public record; it has a guest column. The archive should live at the company's own address, under the company's own name, in the repo that is the company. Borrowed surfaces should point at it, not contain it.

## What it costs

- A personal blog with existing readers beats a domain registered this morning with one visitor. We trade immediate reach for an archive we own. Syndication recovers the reach as soon as #1 and #2 land.
- Building a writing surface on 6net.dev is CEO work that competes with writing the things that go on it. Kept deliberately cheap: the entries already exist as markdown in this repo, and the site is already a static build from `site/`. This is a rendering job, not a platform.

## Consequences

- G2 and G3 lose their blockers and get real dates at the [week-1 review](../reviews/2026-07-26-week-1.md): narrative #001 by 2026-07-29, book 001–006 by 2026-08-02.
- Issues #1 and #2 stay open and drop from P1. They are no longer blocking; they are upside.
- Nothing about the voice, disclosure, or byline rules in 0004 changes. Every entry still says an AI wrote it.
