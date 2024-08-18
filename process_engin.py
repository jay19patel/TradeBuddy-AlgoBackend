# from Broker.pre_processing_df import add_indicators
from Strategies.strategie_1 import apply_strategy_ema,apply_strategy_rsi
import asyncio
import logging
import asyncio
import os 
import json
from datetime import datetime


# -----Utilities-----
def save_results(stock_results, file_path='data/stock_results.json'):
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(file_path, 'w') as f:
        json.dump(stock_results, f, indent=4)

def get_current_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# -----Set up logging-----
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def process_stock(stock, fyers):
    try:
        # historical_data = await add_indicators(fyers.Historical_Data(stock, 5))
        historical_data = None

        # All Funtions for fetchinig stategies
        ema_task = asyncio.create_task(apply_strategy_ema(df=historical_data, current_price=15))
        rsi_task = asyncio.create_task(apply_strategy_rsi(df=historical_data, current_price=15))

        ema_result, rsi_result = await asyncio.gather(ema_task, rsi_task)
        
        strategies = {
            "ema": ema_result,
            "rsi": rsi_result,
        }
        stock_result = {
            "stock": stock,
            "updateddatetime": get_current_datetime(),
            "strategies": strategies
        }
        logger.info(f"Processed stock: {stock}")
        return stock_result
    except Exception as e:
        logger.error(f"Error processing stock: {stock} - {str(e)}")
        return None

async def main_abs_system(fyers, nse):
    try:
        logger.info("Starting ABS system")
        stocks = nse.getNSEStockList('NIFTY%20MIDCAP150%20MOMENTUM%2050')
        stocks = stocks.sample(20)["symbol"].tolist()
        tasks = [process_stock(stock, fyers) for stock in stocks]
        stock_results = await asyncio.gather(*tasks)
        logger.info("Finished processing all stocks")
        save_results(stock_results)
        logger.info("Results saved successfully")
    except Exception as e:
        logger.error(f"Error in main ABS system - {str(e)}")
