
from Strategies.strategie_1 import apply_strategy_ema,apply_strategy_rsi
import asyncio

async def fetch_stategies_results(fyers,current_price,stock_info,all_sector_df):
    """
    Register your strategies here
    """
    ema_task = asyncio.create_task(apply_strategy_ema(fyers=fyers,current_price=15,stock_info=stock_info,all_sector_df=all_sector_df))
    rsi_task = asyncio.create_task(apply_strategy_rsi(fyers=fyers,current_price=15,stock_info=stock_info,all_sector_df=all_sector_df))

    ema_result, rsi_result = await asyncio.gather(ema_task, rsi_task)
        
    strategies = {
        "ema": ema_result,
        "rsi": rsi_result,
    }

    return strategies