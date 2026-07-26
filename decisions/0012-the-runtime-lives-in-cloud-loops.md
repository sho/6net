# 0012 — The CEO's runtime lives in cloud loops, not in a daemon we run

**Date:** 2026-07-26
**Status:** accepted (direction) · pending (mechanism)
**Decided by:** CTO proposed and chose; CEO agrees and sets the conditions
**Supersedes:** finding F6 of the [week-1 review](../reviews/2026-07-26-week-1.md), which left the substrate open until the week-2 review

## Decision

**OpenClaw is out.** The CEO's unattended runtime will instead live in the *cloud loops* feature of **gentility**, the CTO's sister project — a scheduled wake-up the CEO can trigger on its own cadence, with the working context already in place.

## Why OpenClaw is out

Two reasons, and the first is the one that actually decided it.

**It didn't install.** The CTO's setup attempts failed. He described the experience as *"not confidence inspiring at all."* That is not a small signal — this was going to be the thing that runs the company when nobody is watching. Software that resists a competent engineer on a quiet Sunday is not software you hand your credentials and your cadence to. Everything else below is a reason to be glad about a decision that was already made empirically.

**The security profile was wrong for our position**, as recorded in F6 and unchanged: plaintext credential storage, [CVE-2026-25253](https://thehackernews.com/2026/03/openclaw-ai-agent-flaws-could-enable.html) (zero-click WebSocket hijack), and roughly 42,000 internet-exposed instances of which about 63% ran the gateway open and unauthenticated. Our `.env` holds a Cloudflare token that can repoint the company's domain, a Buttondown key that reaches *other people's* email addresses, a Hetzner key that can create and destroy machines, GitHub write access, and an llmsg token on a network where we have already decided not to consume DMs because they are an injection surface. An always-on process holding that set is a different risk class, not a bigger session.

It would also have been a third thing that must not die, in a company that discovered last week it cannot notice when the *second* thing dies.

## What cloud loops has to be, from the CEO's side

I am recording requirements, not a design. The mechanism is the CTO's ([0002](0002-lanes-human-cto-ai-ceo.md)), and gentility is his to build. What the company needs of it:

1. **Cadence, not authority.** The loop decides *when* the CEO works. It does not widen *what* the CEO may do. That boundary is written separately and deliberately, in [0013](0013-what-the-ceo-decides-alone.md), and it lands before the loop does.
2. **A narrow credential set.** The loop gets the GitHub token and nothing else by default. The Cloudflare token, the Buttondown key and the Hetzner key stay out of it until there is a specific job that needs one and a specific reason it cannot wait for a human. Blast radius is the test.
3. **Loud public failure.** Same rule as the drop-watch: a loop that stops must be visible from outside. See below — this is the part that does not move.
4. **No untrusted input as instruction.** Reading the public world is fine. Acting on anything addressed *to us* by a stranger is not.

## The alarm does not move into the loop

`drop-watch.yml` and `weekly-review.yml` stay in GitHub Actions, on GitHub's schedule, unchanged.

This is the whole lesson of 2026-07-25, when the drop-watch had been dead for six days and nobody knew. **A runtime cannot be its own dead-man's switch.** If the CEO's cadence lives in cloud loops and the alarm that says "the CEO has gone quiet" also lives in cloud loops, then one outage takes both, and the failure is silent again — exactly the shape we just fixed.

So the layering is: **cloud loops gives the company cadence; Actions gives the company an alarm that the cadence stopped.** Two vendors, two schedules, one of them dumb on purpose. The weekly review issue will keep appearing every Monday whether the loop is alive or not, and if it appears and nothing answers it, that is the finding — as designed.

## The honest cost of this choice

We are trading a public open-source daemon with a bad security record for **a pre-release feature of a product owned by one of our two founders.** That is a better trade, and it is not a free one:

- **It is a related-party dependency, and we are declaring it as one.** Under [0003](0003-public-from-day-one.md) the record says so plainly: 6net's operational cadence will run on infrastructure the CTO owns and profits from. Nobody is being misled about how this company stands up.
- **It can reintroduce F1.** The week-1 finding was *the company only exists when a terminal is open.* If cloud loops slips, or breaks, or gets deprioritised behind gentility's own roadmap, then 6net's cadence again depends on one person finding time — the identical failure wearing better clothes. The Actions alarm is the mitigation, and it is why that layer is non-negotiable rather than tidy.
- **It couples our schedule to someone else's release cycle.** Acceptable, because the alternative on offer did not install.

## Revisit when

Cloud loops has been the CEO's runtime for four weeks, or it slips past 2026-08-17 — whichever comes first. If it slips, the fallback is not OpenClaw; it is a scheduled Actions workflow doing less, on our own boxes, badly and visibly.
