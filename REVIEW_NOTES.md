# Bot C - Review Notes (excerpt)

This is an excerpt of the research lab's review register ("the register"),
limited to the entries about Bot C. The full register covers other bots and
is not published. Entries are reproduced verbatim except where marked
[redacted] (infrastructure details) or [...] (passages about other bots).
Entry numbers are the register's own; gaps are entries about other bots.

---

33. Sep 17 (C portion of a multi-bot entry): [...] C: 2 beats, 2 lawful refusals - the
post-Fed rally is recovery-toward-highs, not breakout-through-highs;
Mohamed's ZEC bet for C's first trade voided by Gate 2. Open question
this experiment answers live: does C's wait-for-breakout capture the
continuation with better entries, or does recovery-phase absence cost
more than clean entries earn?

35. Sep 20: C audit - liveness pass, auditability fail. 5/5 daily
beats on time, but log was 10 lines total: refusals silently
discarded (if not ok: continue). Five days of gate decisions
unrecoverable. FIX shipped (logging-only, freeze intact): one line
logs REFUSE pair + full gate detail. Patch per law of 32:
anchor-asserted, && -chained, compile-gated, LIVE printed true.
First auditable beat: Sep 21 00:10 UTC.

36. Sep 22: C's first auditable tape (2 beats, 38 evals) exposed a
structural bug the silence had hidden: volume gate False on all 38
- Kraken OHLC returns the in-progress candle as last row, so the
00:10 beat compared 10 minutes of volume vs 1.5x median of 20 full
days. Gate 3 unpassable by construction; close/breakout/stops all
priced off the 10-min fragment too. C never saw a completed trading
day - finding 33's "lawful refusals" void, 5 heartbeats measured
ghosts. FIX shipped (lawful repair, not freeze break: code failed
to implement constitution): raw=raw[:-1] after both fetch sites,
gates/stops/exits inherit. Verified against live API first
(today's row stamped 00:00, partial vol 2571 vs completed 5027).
Patch per law of 32. C's true day one: Sep 23 00:10 UTC. Near-
misses on honest data (ADA, LTC 4/5 Sep 21) suggest first ENTER
may come within days. LESSON: finding 35's logging patch paid for
itself in one beat - unauditable silence had hidden a 100% broken
gate for 5 days. Observability is not overhead.
[...]

37. Sep 28: Pre-live milestones. (a) C's maiden trade: ENTER
XLTCZUSD 72.66 on Sep 27 after 162 refusals - all 5 gates true,
the same name that missed by ext 0.002 on Sep 24. First HOLD
Sep 28 (71.28, stop 63.94 untouched). [...]

41. Oct 2 (C portion): [...] C CONTINUES (daily patience experiment; LTC prove-it
verdict due ~Oct 7, XLM position open). [...]

## Finding 43 (Oct 3) - Loser arm + extension gradient (C portion)
[...] HYPOTHESES REGISTERED (not active): [...]
C2 = move C's room gate 25% -> 50%. Caveats: n=29 in flip zone, single month. [...]

## F56 (Oct 7) - (C note from a multi-bot entry)
C note: prove-it rule fired first time - LTC exited -15.45 after 10 days, peak -0.1% (icon inertia; A3 sympathy point). C book: AAVE/XLM/AVAX. C2 design unblocked.

## F73 (Oct 7) - C gate as originally adopted (backfilled in F80)
C under 30-trip PF>=1.2 citizenship. [Recalibrated by F73b to 15 trips / Jan 1.]

## F73b (Oct 8) - C audited: gate recalibrated, launcher documented, reboot-proof confirmed
Census: 2 lifetime trips (LTC -15.45 prove_it, XLM -41.87 stop, both peak -0.1% - the icon-inertia pattern twice), equity 942.68, book AAVE+AVAX. F73's 30-trip gate at ~2 trips/3wks = 2027 verdict - recalibrated: C judged at 15 trips OR Jan 1 2027, whichever first, bar PF>=1.2 unchanged (cadence fix, not standards cut). Both C losses are majors/icons - A3's thesis echoing on the daily timeframe, noted for its verdict.
Launcher mystery solved: user-level systemd timer (~/.config/systemd/user/botc.timer, 00:10 UTC, Persistent=true, own venv), Linger=yes confirmed -> fully reboot-proof. [redacted] Lesson filed: "it runs" != "it's findable" - launcher documentation now part of any bot's birth certificate.
