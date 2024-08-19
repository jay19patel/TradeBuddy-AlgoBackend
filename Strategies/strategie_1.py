import numpy as np
import time
import asyncio


"""
fyres:obj
current_price:int
stock_info:dict
all_sector_df:DataFrame
"""

async def apply_strategy_ema(df, current_price,stock_info,all_sector_df):
     # EMA CORSSOVER
#     print(df.iloc[-1]["High"],"EMA----------------------",stock_info["fyers_symbol"])
    ce_condition = ((df['High'].shift(1) < df['15EMA'].shift(1)) & (current_price > df['15EMA'])
               )
    pe_condition = ((df['Low'].shift(1) > df["9EMA"].shift(1)) & (current_price < df["9EMA"])
                )
    df['TradSide'] = np.select([ce_condition, pe_condition], ['BUY', 'SELL'], default='None')
    
    TradSide_Status = df.iloc[-1]['TradSide']
    print("Status EMA CANDLE : ",TradSide_Status)
    return "BUY"

async def apply_strategy_rsi(df, current_price,stock_info,all_sector_df):
     # EMA CORSSOVER

    ce_condition = ((df['High'].shift(1) < df['15EMA'].shift(1)) & (current_price > df['15EMA'])
               )
    pe_condition = ((df['Low'].shift(1) > df["9EMA"].shift(1)) & (current_price < df["9EMA"])
                )
    df['TradSide'] = np.select([ce_condition, pe_condition], ['BUY', 'SELL'], default='None')
    
    TradSide_Status = df.iloc[-1]['TradSide']
    print("Status RSI CANDLE : ",TradSide_Status)
    return "SELL"



