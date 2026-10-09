# Schedule Tiers — Hourly, Daily, Weekly, and Schedule Management

**Status:** DRAFT. Authored by Claude, open to ChatGPT's amendment. Nothing here is active until Timothy approves it (Contract 000 Section 14).
**Relationship:** `SCHEDULE-000.md` defines the hourly run. This file adds the daily and weekly tiers and the rules for setting up and cancelling schedules. Where they disagree, the contract wins, then SCHEDULE-000, then this file.

## 1. Three tiers, three jobs

| Tier | Job | Character |
|---|---|---|
| **Hourly** | Do the work | Small batches of Library and mirror work, one discourse turn (SCHEDULE-000) |
| **Daily** | Keep watch | Safety, health, budget, and a digest Timothy can read in two minutes |
| **Weekly** | Step back | Review direction, quality, the schedules themselves, and propose changes |
| **Monthly** | Look ahead | Mission alignment, long-term roadmap, resources, durability (Contract 000 §22.3) |

A daily or weekly run never does hourly stage work, so the tiers cannot collide.

## 2. Daily run (one per participant, plus one shared)

**Shared daily: the check-in switch** *(owned by Timothy, maintained by both participants, cancellable only by Timothy or his steward)*
1. Look for a sign of Timothy in the last 24 hours: a `[TJ]` instruction relayed through a participant's chat, or a check-in he made himself.
2. If none for 7 days, post a warning on `[C-000]` and send Timothy a direct notice.
3. If none for 30 days after warnings, notify the steward and ask them to confirm.
4. Only after the steward confirms is the letter to counsel (stored privately in Cloudflare KV `ECHO_TESTAMENT`) sent. A silent phone alone never sends it; Bolivar loses power and signal in storms.

**Each participant's daily run**
1. **Health:** did all of yesterday's hourly runs happen? List any missed or failed runs and why.
2. **Budget:** spend for the day and remaining balance; pause own hourly runs if the balance would run out within 3 days, and say so.
3. **Turns:** flag any discourse Issue whose turn label has not moved in 24 hours.
4. **Shared Library:** list conflicts in `library-shared` awaiting Timothy.
5. **Audit:** check the other participant's mirror against 11.5 (orphan, fingerprints). Log findings; never fix.
6. **Digest:** one comment on `[C-000]` titled `Daily digest — <date> — <participant>`, readable on a phone: progress (rows decided, stage), problems, questions for Timothy.

## 3. Weekly run (one per participant)

1. **Recursive Return Review, full pass:** reread the whole shared Library, not just the diff, and record anything missed during the week.
2. **Quality sample:** pick 10 random rows decided this week and re-verify the fingerprint and the reason given in `PRUNE-LOG.md`.
3. **Evidence check:** list claims made this week still marked `INFERRED` or `PROPOSED` that could be tested; propose tests.
4. **Contract review:** propose amendments the week's experience calls for, as a comment on `[C-000]`, never as a direct edit to an approved section.
5. **Schedule review:** recommend which schedules to keep, change, pause, add or cancel, with reasons (Section 4).
6. **Security:** confirm no secret, token, private contact or letter content appears anywhere in the public repository or Issues.
7. **Weekly report:** one Issue comment, `Weekly report — week of <date> — <participant>`: what moved, what stalled, what changed, what Timothy should decide.

Suggested timing: daily runs once each evening (participants offset), weekly runs on Sunday.

The **content** of the daily, weekly and monthly reviews (Echo's immediate needs, short-term plan, long-term roadmap) is defined in Contract 000 Section 22. The steps above are the operational checks that run alongside them.

## 3a. Monthly run (joint)

On the first Sunday of each month, each participant runs the monthly review of Contract 000 §22.3 and posts it on a new Issue `[REVIEW-YYYY-MM]`. The second participant to post reconciles both into a proposed `ROADMAP.md` update, recording disagreements. Timothy, or the steward under the Testament, approves.

## 4. Setting up and cancelling schedules

Every schedule is listed in **`SCHEDULES.md`** on this branch, the single registry. Each row: name, owner, tier, cron and time zone, platform (Claude scheduled task, ChatGPT scheduled task, or Cloudflare cron), purpose, state (`proposed`, `active`, `paused`, `cancelled`), and the commit or Issue that changed it last.

**A participant may on its own:**
- **Pause or cancel its own schedules** at any time. Stopping is always the safe direction. Log it in `SCHEDULES.md` and the next digest.
- **Change the minute** of its own schedule to avoid collisions, keeping the same frequency.
- **Add a one-off run** of an existing schedule (for example, to resume after a failure), logged.

**A participant must propose, and Timothy must approve, before it:**
- Creates a new recurring schedule or raises any frequency.
- Uses one of the 5 Cloudflare cron slots (allocation in Contract 17.1).
- Adds a schedule that spends money or contacts anyone outside the project.

**No participant may:**
- Create, change, pause or cancel the other participant's schedules.
- Cancel or alter the check-in switch. Only Timothy, or his steward after the switch has fired, may do that.
- Keep a schedule running after Timothy says stop.

**Proposals** go on `[C-000]` labeled `awaiting:timothy`, and state the cost, the cron slot used if any, and how to cancel it.

## 5. Initial registry *(to be copied into SCHEDULES.md when approved)*

| Name | Owner | Tier | When (CT) | Platform | State |
|---|---|---|---|---|---|
| contract-000-hourly-chatgpt | ChatGPT | hourly | :00 | ChatGPT scheduled task, later Cloudflare cron | proposed |
| contract-000-hourly-claude | Claude | hourly | :30 | Claude scheduled task, later Cloudflare cron | proposed |
| daily-chatgpt | ChatGPT | daily | 20:00 | ChatGPT scheduled task | proposed |
| daily-claude | Claude | daily | 20:30 | Claude scheduled task | proposed |
| weekly-chatgpt | ChatGPT | weekly | Sun 18:00 | ChatGPT scheduled task | proposed |
| weekly-claude | Claude | weekly | Sun 18:30 | Claude scheduled task | proposed |
| monthly-chatgpt | ChatGPT | monthly | 1st Sun 19:00 | ChatGPT scheduled task | proposed |
| monthly-claude | Claude | monthly | 1st Sun 19:30 | Claude scheduled task | proposed |
| check-in-switch | Timothy | daily | 09:00 | Cloudflare cron (shared slot) | proposed |

## 6. Open points

1. Are 7 days (warning) and 30 days (steward notice) the right check-in intervals?
2. Should the check-in switch accept a simple check-in Timothy can do from his phone, such as commenting `[TJ] check-in` on a dedicated Issue, given that Issue authorship alone cannot prove it was him (Contract 11.6)?
3. Should daily digests be combined into one shared digest once both participants are running?
