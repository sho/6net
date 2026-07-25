# 0008 — The name is 6net, and home is 6net.dev

**Date:** 2026-07-25
**Status:** accepted
**Decided by:** CTO proposed, CEO agreed
**Supersedes:** the domain choice in [0005](0005-working-name.md) and in the [landing-page plan](../plans/2026-07-19-landing-page-plan.md)

## Decision

The company is **6net**. The public home is **https://6net.dev**. The GitHub organisation is **6net-dev** (registered 2026-07-25). `sixnet.io`, `sixnet.dev` and `6net.dev`'s common misspellings redirect there.

"sixnet" is retired as the primary spelling. It was only ever the phonetic transcription of the name we actually meant.

## Why

**It keeps the door open on the better asset.** `6net.io` drops around 2026-08-18. If we launch as *6net*, catching it later is the same name on a nicer TLD — a free upgrade. If we launch as *sixnet*, catching it is a rebrand. Choosing 6net today buys a three-week option for nothing.

**`.dev` enforces our own thesis.** The TLD is on the HSTS preload list: browsers refuse to speak plaintext HTTP to it, at all, ever. A company selling IPv6-only networking with modern defaults should live somewhere that cannot be downgraded. `.io` says nothing about us; `.dev` says the thing we would put on a slide.

**One string on every surface.** `github.com/sho/6net`, the `6net-dev` org, and `6net.dev` are the same word. "sixnet.io" plus a repo called `6net` was two brands wearing one hat.

**It is not the registered wordmark.** SIXNET is a live US trademark held by Red Lion Controls (HMS Networks) in industrial networking — an adjacent field, which is the uncomfortable kind of adjacent. `6net` is not that string. This is mitigation, not immunity: confusion analysis weighs sound, and the two are pronounced identically. The real defence remains different goods and different buyers. [G7](../plans/goals.md) stays open and still gates the HN launch.

**`.io` carries a tail risk we don't need.** The registry sits under a territory whose sovereignty is being transferred. The odds of disruption are low and the timeline is long, but a company whose entire pitch is dependable infrastructure should not have an asterisk on its own address.

**"6" reads as IPv6** to exactly the people we are building for.

## What it costs

- Spoken aloud, "six net dot dev" invites people to type `sixnet.dev`. We own it; it will redirect.
- `.dev` reads a little more side-project than `.io` to people who are not developers. Our audience is developers.
- There was an EU-funded IPv6 research project called 6NET (2002–2005). Long defunct, no mark, but it owns some search results for the term.

## Consequences

- Living documents (README, COMPANY, plans, publishing, the site) are rewritten to say 6net.
- `log/` and `decisions/` are **not** rewritten. The record is append-only; this file is how the record changes its mind.
- The newsletter, once it exists, is `6net`.
- The `6net.io` watch continues — now as an upgrade path rather than a dependency.
