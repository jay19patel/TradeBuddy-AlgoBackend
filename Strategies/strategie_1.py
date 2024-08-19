import numpy as np
import time
import asyncio


"""
fyres:obj
current_price:int
stock_info:dict
all_sector_df:DataFrame
"""

async def apply_strategy_ema(fyers, current_price,stock_info,all_sector_df):
    await asyncio.sleep(5)  # use await instead of asyncio.sleep
    return "BUY"

async def apply_strategy_rsi(fyers, current_price,stock_info,all_sector_df):
    # Implement RSI strategy logic
    await asyncio.sleep(4)  # use await instead of asyncio.sleep
    return 'SELL'



