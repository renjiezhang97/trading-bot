"""moomoo (Futu OpenAPI) broker layer.

Connects to a locally running OpenD gateway. Connection settings come
from environment variables (see .env.example) so nothing sensitive
lives in the repo.

Requires:  pip install moomoo-api python-dotenv
"""

import os

from dotenv import load_dotenv
from moomoo import (
    OpenQuoteContext,
    OpenSecTradeContext,
    TrdEnv,
    TrdMarket,
    TrdSide,
    OrderType,
    RET_OK,
)

load_dotenv()

HOST = os.getenv("MOOMOO_HOST", "127.0.0.1")
PORT = int(os.getenv("MOOMOO_PORT", "11111"))
TRD_ENV = TrdEnv.SIMULATE  # paper trading


class Broker:
    def __init__(self):
        self.quote_ctx = OpenQuoteContext(host=HOST, port=PORT)
        self.trade_ctx = OpenSecTradeContext(
            filter_trdmarket=TrdMarket.US, host=HOST, port=PORT
        )

    def get_quote(self, symbol: str) -> float | None:
        """Return the last price for a symbol like 'US.QQQ'."""
        ret, data = self.quote_ctx.get_market_snapshot([symbol])
        if ret != RET_OK:
            print(f"quote error: {data}")
            return None
        return float(data["last_price"][0])

    def buy(self, symbol: str, qty: int) -> bool:
        ret, data = self.trade_ctx.place_order(
            price=0,
            qty=qty,
            code=symbol,
            trd_side=TrdSide.BUY,
            order_type=OrderType.MARKET,
            trd_env=TRD_ENV,
        )
        if ret != RET_OK:
            print(f"order error: {data}")
            return False
        print(f"BUY {qty} {symbol} submitted (order_id={data['order_id'][0]})")
        return True

    def sell(self, symbol: str, qty: int) -> bool:
        ret, data = self.trade_ctx.place_order(
            price=0,
            qty=qty,
            code=symbol,
            trd_side=TrdSide.SELL,
            order_type=OrderType.MARKET,
            trd_env=TRD_ENV,
        )
        if ret != RET_OK:
            print(f"order error: {data}")
            return False
        print(f"SELL {qty} {symbol} submitted (order_id={data['order_id'][0]})")
        return True

    def close(self):
        self.quote_ctx.close()
        self.trade_ctx.close()
