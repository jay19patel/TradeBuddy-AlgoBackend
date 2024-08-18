
from Strategies.strategie_1 import apply_strategy_ema,apply_strategy_rsi
import asyncio

async def fetch_stategies_results(historical_data , current_price):
    ema_task = asyncio.create_task(apply_strategy_ema(df=historical_data, current_price=15))
    rsi_task = asyncio.create_task(apply_strategy_rsi(df=historical_data, current_price=15))

    ema_result, rsi_result = await asyncio.gather(ema_task, rsi_task)
        
    strategies = {
        "ema": ema_result,
        "rsi": rsi_result,
    }

    return strategies