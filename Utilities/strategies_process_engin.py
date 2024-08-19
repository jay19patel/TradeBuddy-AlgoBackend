
# Custom 
from Strategies.strategies_result_execution import fetch_stategies_results
# from Utilities.pre_processing_df import add_indicators
from Core.config import setting
from Utilities.fyers_utility import convert_nse_symbol_to_fyers_symbol
# Inbuild
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

async def process_stock(stock, fyers,live_prices,stocks_df):
    try:
        # historical_data = await add_indicators(fyers.Historical_Data(stock, 5))
        historical_data = None
        current_price = live_prices.get(stock.split(":")[1])     
        # All Funtions for fetchinig stategies
        strategies = await fetch_stategies_results(historical_data=historical_data,current_price=current_price)
        
        stock_result = {
            "stock": stock,
            "updateddatetime": get_current_datetime(),
            "current_price":current_price,
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
        main_indexis = ["NIFTY50","NIFTYBANK"]
        stocks_df = nse.getNSEStockList("NIFTY%20MIDCAP150%20MOMENTUM%2050")
        stocks_symbol_list = stocks_df.sample(20)["symbol"].tolist()
        stocks_symbol_list.extend(main_indexis)
        stocks_symbol_list = convert_nse_symbol_to_fyers_symbol(stocks_symbol_list)

        live_prices = await fyers.get_current_ltp(stocks_symbol_list)

        tasks = [process_stock(stock, fyers,live_prices,stocks_df) for stock in stocks_symbol_list]

        stock_results = await asyncio.gather(*tasks)
        logger.info("Finished processing all stocks")
        save_results(stock_results)
        logger.info("Results saved successfully")
    except Exception as e:
        logger.error(f"Error in main ABS system - {str(e)}")
