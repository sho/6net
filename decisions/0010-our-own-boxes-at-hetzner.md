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
