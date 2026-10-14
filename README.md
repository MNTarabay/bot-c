# Bot C — Daily Trend-Following Research Bot (Kraken, paper trading)

**Author and research lead:** Mohamed Tarabay
**Implementation:** Claude Code (Anthropic), working to the author's specifications

## What this is

Bot C is one bot from a small algorithmic-trading research lab I run on Kraken. It is a daily-timeframe trend-following strategy over Kraken USD spot pairs, running in paper-trading mode on a Linux server via a daily `systemd` timer.

I am publishing it as evidence of how I work, not as a trading product. The code was written by an AI coding agent. I did not write it, and I do not claim to be a programmer. What I did was everything around the code:

- Designed the strategy and chose the universe, timeframe, entry and exit logic.
- Wrote `CONSTITUTION.md` before any code existed: the rules the bot must obey and the go-live thresholds that lock at its first trade.
- Designed the experimental protocol for the lab as a whole: a frozen control bot, single-change paper-trading clones, pre-registered hypotheses, and written evidence gates that must be cleared before any capital is committed or scaled.
- Read every result, maintained the lab register (`REVIEW_NOTES.md` here is the Bot C excerpt), issued verdicts, and directed each upgrade.

If you want to judge my work, read the constitution and the review notes. If you want to judge the code, judge the agent.

## Why it was built this way

My background is in finance research, specifically machine-learning early-warning systems for bank systemic risk. The lab exists to test whether that research discipline — pre-registration, controls, honest evaluation, staged commitment under uncertainty — transfers to a live, adversarial environment. The bots are the instrument; the method is the point.

## Repository layout

    CONSTITUTION.md     Rules and go-live thresholds, written before the code
    REVIEW_NOTES.md     Bot C entries from the lab register, with an explanatory header
    src/botc/           Universe, gates, exits and Kraken public-data client
    config/             params.yaml (all strategy parameters) and example.env (path variables)
    scripts/            heartbeat.py daily entry point, botc.service and botc.timer

## Running it

Paper mode only. Requires Python 3.11+ and a Linux host with `systemd`. No Kraken account or API key is needed; the client calls public market-data endpoints only. Install dependencies from `requirements.txt`, set the path variables from `config/example.env`, run `scripts/heartbeat.py` once to verify, and install the service and timer from `scripts/`.

No live-trading code path exists in this bot.

## Status

Paper trading since September 2026. Results and verdicts are in `REVIEW_NOTES.md`. This bot has never traded real funds.

## Licence

MIT. Use at your own risk; nothing here is investment advice.
