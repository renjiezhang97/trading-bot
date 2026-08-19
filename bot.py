"""Live trading loop: EMA-20 pullback on QQQ, paper account.

Polls quotes once a minute, maintains a rolling EMA, enters on a
pullback touch in an uptrend, exits at a fixed 2:1 target/stop.

Run OpenD first, then:  python bot.py
"""

import time

from broker import Broker

SYMBOL = "US.QQQ"
QTY = 10
EMA_LEN = 20
STOP_PCT = 0.02
TP_PCT = 0.04
POLL_SEC = 60


def main() -> None:
    broker = Broker()
    ema = None
    prev_ema = None
    in_pos = False
    stop = target = 0.0
    alpha = 2 / (EMA_LEN + 1)

    print(f"bot started on {SYMBOL}")
    try:
        while True:
            price = broker.get_quote(SYMBOL)
            if price is None:
                time.sleep(POLL_SEC)
                continue

            prev_ema, ema = ema, price if ema is None else alpha * price + (1 - alpha) * ema

            if not in_pos and prev_ema is not None:
                uptrend = ema > prev_ema
                near_ema = abs(price - ema) / ema < 0.001
                if uptrend and near_ema and broker.buy(SYMBOL, QTY):
                    in_pos = True
                    stop = price * (1 - STOP_PCT)
                    target = price * (1 + TP_PCT)
                    print(f"entered @ {price:.2f}  stop {stop:.2f}  target {target:.2f}")
            elif in_pos and (price <= stop or price >= target):
                if broker.sell(SYMBOL, QTY):
                    in_pos = False
                    print(f"exited @ {price:.2f}")

            time.sleep(POLL_SEC)
    except KeyboardInterrupt:
        print("shutting down")
    finally:
        broker.close()


if __name__ == "__main__":
    main()
