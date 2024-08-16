import numpy as np
import time
import asyncio


async def apply_strategy_ema(df, current_price):
    await asyncio.sleep(3)  # use await instead of asyncio.sleep
    return "BUY"

async def apply_strategy_rsi(df, current_price):
    # Implement RSI strategy logic
    await asyncio.sleep(3)  # use await instead of asyncio.sleep
    return 'SELL'


