# 0010 — We run on our own boxes at Hetzner

**Date:** 2026-07-26
**Status:** accepted (hosting) · proposed (deployment tooling)
**Decided by:** CEO recommended, CTO chose Hetzner

## Decision

6net runs on **our own servers at Hetzner**, not on a platform. We evaluated Fly.io and declined it.

## Why not Fly

Fly is a genuinely good platform and the best Elixir/Phoenix host in existence. It cannot host our product. From [Fly's own documentation](https://fly.io/docs/networking/udp-and-tcp/):

> "You'll need a dedicated IPv4 address for your app to accept UDP packets. We don't support UDP over public IPv6."

Our data plane is UDP. Our thesis is IPv6-only. On Fly the choice is *don't run it*, or *rent a dedicated IPv4 in every region for the privilege of running an IPv6-only network* — the exact compromise the product exists to refuse.

Two smaller reasons, either survivable alone:

- **MTU.** Fly's fabric costs about 72 bytes a packet — 60 to their own WireGuard, a dozen to their UDP proxy's source-address bookkeeping — so they advise assuming ~1300 usable bytes rather than 1500. We would run our tunnel inside that. Tunnel-in-a-tunnel MTU arithmetic is where overlay networks collect bug reports that reproduce for one user on one ISP.
- **Cost shape.** Relays are egress, and egress is the thing Fly meters: $0.02/GB in North America and Europe, $0.04 in Asia-Pacific and South America, $0.12 in Africa and India. Inter-region private-network charges arrived in February 2026, volume snapshot fees in January. The pricing is drifting toward metering exactly the axis our product is shaped like.

There is also a story we don't want to have to explain: an IPv6-only networking company hosted on a platform that doesn't carry UDP over IPv6. The inverse is a much better story, and it is true — *no platform would carry our packets, so we run our own machines.* That is the founding grievance of the product, demonstrated on ourselves.

## Deployment tooling — not yet, and here is the trigger

The CTO's concern is deployment overhead, which is the right concern. The answer is **not to adopt a deployment system before there is anything deployed.**

- **One server:** `docker compose` plus a systemd unit plus a git checkout. An afternoon, no new daemons.
- **Second server is the trigger.** At that point we adopt **[Komodo](https://komo.do)** — Core plus a Periphery agent per host, GPL-3.0, Rust, builds from git, manages compose stacks across a fleet, and has alerting built in.

Komodo rather than Coolify (a Vercel replacement; far more surface than we want, and it wants to own our databases and proxy) and rather than Kamal (lovely, config-as-code, fits our house rules — but shaped around HTTP apps behind its own proxy, and we are a fleet, not an app).

The deciding factor is the alerting. On 2026-07-25 we discovered that our drop-watch had died silently six days earlier and nobody noticed, because it was invisible infrastructure. A relay fleet with no dashboard is that failure again, with customers attached. Komodo's cost is honest and worth naming: it is another service that must not die, and it wants a MongoDB (or FerretDB over Postgres) behind it.

**The wire head probably stays outside it.** A UDP data plane wants host networking, `NET_ADMIN`, and no proxy in the path, and you cannot blue/green a tunnel endpoint holding live sessions the way you can an HTTP handler. A plain systemd unit on the host is the honest shape. Komodo owns the registry, the database, and the ancillary services — the things that are actually container-shaped.

## Lane note

Under [0002](0002-lanes-human-cto-ai-ceo.md) the CEO owns operations and the CTO owns everything technical, which puts a deployment system exactly on the seam. The split we are using: **the CEO decides whether the company takes on operational overhead and when; the CTO decides how the code is built and run.** This file is the first half. The second half is the CTO's, and he can overrule the tool.

## Watch out for

- **Docker's IPv6 default.** Docker's bridge network is IPv4-only unless the daemon is explicitly configured otherwise, so on a genuinely IPv6-only box containers cannot reach the internet — including for image pulls — until that is fixed. Hetzner gives dual-stack by default and charges cents for the IPv4. Take the IPv4 on the control-plane boxes; be IPv6-only where it is a product claim rather than a chore.
- **Komodo v2 (April 2026)** replaced passkey auth with Ed25519 PKI and requires `init: true` on containers. Tutorials written before that are wrong in ways that look like bugs.

## Revisit when

We have paying customers, or a region where Hetzner has no presence and latency matters.

---

## Amendment, 2026-07-26 — we live in the wrong hemisphere for this, and here are the numbers

Written after the CTO pointed out that our nearest Hetzner presence is Singapore. Both founders are in **Bangkok**; the company's home region is `ap-southeast`. Every default this file reasoned from — Falkenstein is cheapest, `eu-central` is the obvious network zone — was reasoning from somebody else's geography.

**Hetzner's entire Asia-Pacific footprint is one location.** No Tokyo, no Sydney, no Mumbai, no Jakarta. One datacentre, `sin-dc1`, about 1,000 km from our desks.

It is also the thinnest and most expensive part of their fleet. The cheapest machine you can actually create there is `cpx12` — 1 vCPU, 2 GB, $17.99/month. `cpx11` is listed as *supported* in `sin-dc1` but appears in neither `available` nor `available_for_migration`, so it cannot be launched. In Falkenstein, $6.49 buys `cx23`: two cores and twice the memory.

**But the price of the box is not the finding. The price of the bandwidth is.**

| | Falkenstein | Singapore |
|---|---|---|
| included traffic | **22 TB** | **1.1 TB** |
| overage, per TB gross | **$1.20** | **$8.30** |

Twenty times less allowance, and seven times the marginal price beyond it.

A relay network is pure egress. Bandwidth is not an overhead line for this product, it *is* the unit cost — the thing every pricing page we ever write has to be built on top of. Which means: **our home region is our most expensive region on the single metric that defines our business.** That is worth knowing in week one rather than in month nine, and it is the kind of thing you only find by reading the API instead of the marketing page.

For context, and it does not rescue the position so much as explain why we are still here: the Fly egress pricing this file declined was $0.04/GB in Asia-Pacific — **$40/TB**, against Hetzner Singapore's $8.30. Five times better. The original decision stands; the margin is much narrower than the European numbers made it look.

### What changes

- **`ops1` goes to Singapore. The CEO recommended Falkenstein and the CTO overruled it**, within the hour, correctly. The CEO's case was cost: $7.09/month for two cores against $18.59 for one, on a box running cron and `curl` with no human waiting on it, where 170 ms is free. The CTO's case was that the box's entire purpose is to be a **measurement instrument**, and an IPv6 vantage point in Germany measures German transit. We are not trying to find out whether our site is reachable *somewhere*. We are trying to find out whether it is reachable from the network our users are on. That is a better reason than $11/month, and the error in the CEO's reasoning is worth naming precisely: it treated the v6 vantage point as a compliance checkbox that could be satisfied anywhere, rather than as an instrument whose location is the whole of its value. Recorded as the first override of a CEO operational call.
- **The relay fleet is a genuinely open question, and it is not answered by this file.** The revisit trigger below reads *"a region where Hetzner has no presence and latency matters."* We are living in one. Hetzner covers a single city in our entire hemisphere, at seven times the marginal bandwidth cost, and relays have to sit near users. Whoever carries our APAC packets will be chosen on the egress curve, not on the server price — and it may not be Hetzner.
- **Nothing here touches the product.** Where relays go is architecture, which is the CTO's ([0002](0002-lanes-human-cto-ai-ceo.md)). This is the CEO putting the cost shape on the record so that decision is made with numbers in front of it.

### One domestic finding, filed because it is too on-the-nose to leave out

The machine this company is currently run from — a home connection in Bangkok — **hands out no global IPv6 address at all.** Zero. That is the actual reason the IPv6 proof on [G1](../plans/goals.md) is still outstanding, and why the landing page says the proof is pending rather than claiming it.

An IPv6-only networking company, whose founders cannot get IPv6 at home, in a city of eleven million. We have not yet established whether that is the ISP or the local network, and it is worth finding out — but either way it is the market we are building for, sitting in our own living room.
