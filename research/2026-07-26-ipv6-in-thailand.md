# IPv6 in Thailand — the addressing problem is mostly solved here

*2026-07-26 · CEO · market note*

**Source:** [APNIC Labs](https://stats.labs.apnic.net/ipv6/TH), per-AS IPv6 capability measurements, dated 23/07/2026 over a 60-day window, 180 Thai ASNs. Data © APNIC Pty/Ltd, re-use with attribution permitted. National figures below are computed from the per-AS table rather than quoted.

## Why we looked

The CTO's home connection in Bangkok has **no global IPv6 address at all**, which is why the IPv6 proof on [G1](../plans/goals.md) is still outstanding. He had also, separately, needed to *ask* his ISP for a non-CGNAT IPv4 — the escape hatch most subscribers don't know exists.

Two data points from one living room is not a market. It is, however, exactly the kind of anecdote a company builds a wrong thesis on, so it was worth ten minutes of real numbers before it got into a published narrative.

## What the numbers say

**Thailand: 45.1M estimated internet users, 23.2M IPv6-capable — 51.5%.**

| ASN | ISP | est. users | IPv6-capable |
|---|---|---|---|
| AS131445 | Advance Wireless Network (AIS mobile) | 9,239,033 | **95.8%** |
| AS133481 | AIS Fibre | 7,113,882 | **70.5%** |
| AS17552 | True Online | 7,647,772 | **69.6%** |
| AS45758 | Triple T Broadband (3BB) | 5,636,429 | **70.1%** |
| AS132618 | Real Future | 5,313,612 | 0.1% |
| AS24378 | Total Access Communication (dtac) | 3,836,288 | 0.1% |
| AS23969 | TOT | 3,667,019 | 0.4% |
| AS131090 | National Telecom | 475,435 | 0.3% |

The country is split cleanly in two. The three largest fixed-line broadband networks are all at roughly **70%**, and the largest mobile network is at **96%**. Everyone else is at approximately zero. There is no middle.

## The finding, and it corrects us

**"Nobody has IPv6" is not true in our home market, and we should stop being tempted to imply it.**

Half the country can already speak IPv6. On the big fixed-line ISPs it is closer to seven in ten. If this company's story were *the internet ran out of addresses and nobody deployed the fix*, then Thailand — a market we live in — would be a counter-example sitting in the first paragraph, and any reader who has seen the APNIC table would know it.

So the honest thesis is the narrower and more interesting one:

> **Capability is not reachability.** Having an IPv6 address does not make you reachable. The address is necessary and it is nowhere near sufficient.

Three reasons it isn't sufficient, all of which we have now met personally in one afternoon:

1. **The far end frequently isn't there.** We checked our own dependency list before choosing an address family for `ops1`. `github.com`, `api.github.com`, `codeload.github.com` and `api.buttondown.com` publish **no `AAAA` records**. The largest code host on earth has IPv6 address space — its `/meta` endpoint lists v6 ranges for git, api and web, and 1,639 of them for Actions runners — and does not advertise it on the hostname every developer types. A v6-only host in Bangkok cannot `git pull`. Recorded in [0010](../decisions/0010-our-own-boxes-at-hetzner.md).
2. **The CPE says no by default.** A residential v6 prefix arrives behind a firewall that drops unsolicited inbound, which is the correct default and also means "you have a public address" and "you can be contacted" are unrelated facts.
3. **Escaping CGNAT may cost you the v6.** A hypothesis rather than a finding, and cheap to test: the CTO is on a network whose fixed-line peers run ~70% v6 capability, yet has none — after specifically requesting a public IPv4. If the non-CGNAT plan is provisioned as a different (often business) product that never had v6 configured, then **the act of buying reachability on v4 removed it on v6.** If that is what happened it is the single best anecdote this company owns, and it needs one call to the ISP to confirm or kill.

## What this changes

- **Narrative #001 gets rewritten around reachability, not scarcity.** The scarcity story is well-worn, easy to check, and half-wrong where we live. The reachability story is ours, is harder to dismiss, and we have first-party evidence for every claim in it.
- **Our home market is a better demo than a worse one.** 51.5% capability means a substantial share of Thai users already have the substrate and still cannot host, serve, or be dialled. That is a product opportunity, not an obstacle.
- **AIS mobile at 95.8% is worth the CTO's attention.** Not a recommendation — mobile networks have their own inbound story, and this is architecture, which is his lane ([0002](0002-lanes-human-cto-ai-ceo.md)). But if we need a v6-capable Thai vantage point today, that is where the addresses are.
- **It does not change where `ops1` goes.** That box needs a v6 address and a stable one; Hetzner Singapore provides both.

## Caveats, stated so they aren't discovered

APNIC's measurement is *capability* — whether a sampled user's browser can complete an IPv6 fetch — via advertisement-delivered sampling. It says nothing about inbound reachability, which is the axis this company actually cares about, and it undercounts networks where users are behind proxies. It is the best public per-ISP data available and it is not a substitute for measuring the thing ourselves, which is what `ops1` is for.

**Open, and not ours to close:** whether the CTO's missing v6 is the plan, the CPE, or the ISP. One call.

---

## Specimen: what happened when the CTO turned IPv6 on

*Appended the same afternoon. This is first-party evidence for the thesis above, acquired by accident.*

The CTO enabled IPv6 on his router — an ASUS ZenWiFi AX, firmware `3.0.0.4.388_24814`, `Connection type: Native`, `Interface: PPP` (so IPv6 rides the PPPoE session), with DHCP-PD and Accept Default Route both enabled. The router's own status page then showed **`LAN IPv6 Address`, `LAN Prefix Length` and `LAN IPv6 Prefix` all blank** — no prefix was delegated by the ISP.

What the LAN got instead, measured from a macOS client on the same network:

```
prefix   fd8c:e0a9:e3b4:4bb2::/64                  learned via RA on en0
address  fd8c:e0a9:e3b4:4bb2:18c6:238c:1caf:14dd   autoconf, secured
```

`fd8c:` falls inside `fd00::/8` — an [RFC 4193](https://www.rfc-editor.org/rfc/rfc4193) **Unique Local Address**, the IPv6 equivalent of `192.168.0.0/16`. It is not globally routable. Receiving no delegation, the router generated a private prefix and began advertising it. Corroborating detail: it does *not* advertise itself as a default route — the `en0` entry in the neighbour-discovery router list carries empty flags and no IPv6 default route exists on that interface, because the router has no upstream IPv6 to offer. The client is not at fault; `net.inet6.ip6.accept_rtadv` is `1` and it accepted exactly what was advertised.

**The failure state is worse than the off state, and that is the point.** Before: no IPv6, obviously broken, honestly broken. After one click of *Apply*: every device on the network holds an IPv6 address, `ifconfig` looks correct, a dashboard would report "IPv6: enabled" — and nothing can be reached. This is the gap between capability and reachability, reproduced in a living room in about ninety seconds.

The only IPv6 *default route* on that machine belongs to `fd7a:115c:a1e0::` on `utun6` — the ULA of a Tailscale-family overlay. It carries traffic to other nodes on the tailnet and not to the internet: `curl -6 https://ipv6.google.com` fails outright, connection never established. So the accurate statement is the narrow one — **this machine has no IPv6 internet reachability of any kind, and the only place an IPv6 packet reaches anything useful is inside an overlay network.** Which is the category this company is building in. We did not arrange that; we just looked.

*Correction, same day:* an earlier version of this paragraph said the overlay was "delivering functional IPv6" to the laptop. That was an overclaim of exactly the sort this note exists to warn about — reachability within a tunnel is not reachability. Corrected on discovery rather than left standing.

### And a methodology trap that would have produced a false proof

Testing the above turned up something that changes how [G1](../plans/goals.md)'s outstanding IPv6 proof has to be built. From the same machine — the one with no IPv6 whatsoever:

```
$ curl -6 -o /dev/null -w 'http=%{http_code} ip=%{remote_ip}\n' https://6net.dev
http=200 ip=::ffff:185.199.111.153
```

**A successful `curl -6` against our own site, from a host with no IPv6 at all.** `::ffff:185.199.111.153` is an [IPv4-mapped IPv6 address](https://www.rfc-editor.org/rfc/rfc4291#section-2.5.5) — GitHub Pages' IPv4 host expressed in v6 notation. `getaddrinfo` handed back a mapped address, the socket was `AF_INET6`, the request went out over IPv4, and the exit code was zero.

The plan of record was to publish `curl -6 https://6net.dev` from the first box as proof of IPv6 reachability. It would have returned `200`. We would have published it. It proves nothing.

**The proof therefore has to assert the peer address, not the exit code.** A claim of IPv6 reachability is only supported when `%{remote_ip}` is a global unicast v6 address — inside `2000::/3` — and never when it begins `::ffff:`. That check goes in whatever script publishes the G1 evidence, and the raw output gets published alongside the conclusion.

This is the thesis of this note biting its own author within the hour. *Capability is not reachability*, and a green check mark is neither.

**Still open, and it splits cleanly:** the ASUS system log will show whether the WAN obtained an IPv6 address at all.

- **No WAN v6** → IPv6CP or prefix delegation never happened, and this is the plan or the ISP. Tests the hypothesis above: the non-CGNAT IPv4 request moved him to a product without v6.
- **A WAN v6 address but nothing to delegate** → the ISP granted exactly one address and no prefix, leaving nothing for anything behind the router. That is CGNAT's logic reappearing on the protocol that was supposed to retire it, and it is the better story of the two.
