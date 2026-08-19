"""Toy EMA-pullback backtest on QQQ daily bars.

Educational skeleton: textbook EMA-20 pullback entry, fixed 2:1
take-profit / stop-loss, one position at a time, no costs modeled.
Data comes from yfinance (free, daily bars).

Run:  python backtest.py
"""

import yfinance as yf
import pandas as pd

SYMBOL = "QQQ"
EMA_LEN = 20
STOP_PCT = 0.02      # 2% stop
TP_PCT = 0.04        # 4% target (2:1)
START = "2018-01-01"


def load_data(symbol: str) -> pd.DataFrame:
    df = yf.download(symbol, start=START, auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df["ema"] = df["Close"].ewm(span=EMA_LEN, adjust=False).mean()
    return df.dropna()


def run_backtest(df: pd.DataFrame) -> pd.DataFrame:
    trades = []
    in_pos = False
    entry = stop = target = 0.0

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]

        if not in_pos:
            # Toy entry: price pulled back to touch the EMA while the
            # EMA is still rising (uptrend intact).
            uptrend = row["ema"] > prev["ema"]
            touched = row["Low"] <= row["ema"] <= row["High"]
            if uptrend and touched:
                entry = row["ema"]
                stop = entry * (1 - STOP_PCT)
                target = entry * (1 + TP_PCT)
                in_pos = True
        else:
            if row["Low"] <= stop:
                trades.append({"date": row.name, "pnl_pct": -STOP_PCT * 100})
                in_pos = False
            elif row["High"] >= target:
                trades.append({"date": row.name, "pnl_pct": TP_PCT * 100})
                in_pos = False

    return pd.DataFrame(trades)


def main() -> None:
    df = load_data(SYMBOL)
    trades = run_backtest(df)
    if trades.empty:
        print("No trades.")
        return
    wins = (trades["pnl_pct"] > 0).sum()
    print(f"Symbol:      {SYMBOL}")
    print(f"Trades:      {len(trades)}")
    print(f"Win rate:    {wins / len(trades):.1%}")
    print(f"Total P&L:   {trades['pnl_pct'].sum():.1f}% (sum of per-trade %)")


if __name__ == "__main__":
    main()
