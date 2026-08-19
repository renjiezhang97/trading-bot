# trading-bot

EMA-pullback trading system for US equities, running against the
moomoo (Futu) OpenAPI.

## Structure

- `backtest.py` — historical test of the entry/exit rules on daily bars
- `broker.py` — moomoo OpenD connection, quotes, and order placement
- `bot.py` — live loop: poll quotes → signal → order

## Strategy

Trend-following pullback: when price pulls back to a rising EMA-20,
enter long; exit at a fixed 2:1 reward/risk bracket.

## Setup

1. `pip install -r requirements.txt`
2. Install and run [OpenD](https://www.moomoo.com/download/OpenAPI), log in
3. `copy .env.example .env` and fill in your gateway settings
4. `python backtest.py` to check the historical stats
5. `python bot.py` to run live (paper account)
