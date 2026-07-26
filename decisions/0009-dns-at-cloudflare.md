# 0009 — DNS at Cloudflare, registration stays at Porkbun

**Date:** 2026-07-26
**Status:** accepted
**Decided by:** CTO chose the provider, CEO decided the shape
**Supersedes:** the Porkbun-API dependency (B2) in the [landing-page plan](../plans/2026-07-19-landing-page-plan.md)

## Decision

All 6net domains are managed at **Cloudflare**: `6net.dev`, `sixnet.dev`, `sixnet.io`, and `6net.io` if we catch it.

Three implementation calls that follow from that, which are mine:

1. **Registration stays at Porkbun.** We move nameservers, not registrations. A transfer buys nothing we need, costs a 60-day lock, and is a live-domain operation done for tidiness rather than benefit. Registrar and DNS being different vendors is a mild resilience win: losing one account does not lose both.
2. **The apex is unproxied — grey cloud — for now.** GitHub Pages cannot complete its certificate challenge from behind Cloudflare's proxy, and Cloudflare's default *Flexible* SSL mode plus Pages' HTTPS enforcement is a redirect loop. Unproxied also means visitors resolve GitHub's own `AAAA` records, so the IPv6 claim we publish is about our host and not about somebody's proxy. If we later want the proxy, the mode must be **Full (strict)** and it goes on *after* the certificate exists.
3. **The `sixnet.*` redirects are Cloudflare Redirect Rules**, on proxied placeholder records. Those hostnames serve nothing; a proxy in front of nothing is exactly what they are for.

## Why

Cloudflare's DNS is free, fast, scriptable with a scoped API token, and it is where the rest of the edge lives if we ever need one — redirects, analytics, WAF, Workers — without adding a vendor later. Porkbun's DNS is fine and its API is fine; it just isn't a place anything else grows from.

The token we use is scoped to these zones and to DNS plus redirects. It is not an account key. It never enters this repo — credentials are one of the two standing exclusions in [0003](0003-public-from-day-one.md).

## What it costs

- One more vendor in the critical path of whether the company's website resolves. Cloudflare is a better-than-average bet to hold that position, and DNS is the layer where switching is cheapest — it is a nameserver change away.
- Centralising DNS at the world's largest reverse proxy is a slightly funny look for a company whose product is about not routing everything through one intermediary. We are not proxying traffic through it. The distinction is real and we should be able to say it out loud.

## Consequences

- **B2 changes**: the ask is no longer a Porkbun API key. It is (a) nameservers pointed at Cloudflare and (b) a scoped Cloudflare API token, sent privately.
- **B4 gets cheaper to answer**: Cloudflare Web Analytics is free and works via a JS beacon without proxying. It is the fallback if Plausible's public dashboard isn't worth $9/mo. Still not blocking.
- Cloudflare becomes the place `6net.io` lands if the drop catch works.
