
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

async def process_stock(stock,fyers,live_prices,all_sector_df):
    try:

        strategies = await fetch_stategies_results(fyers=fyers,
                                                   current_price=live_prices,
                                                   stock_info=stock,
                                                   all_sector_df=all_sector_df
                                                   )
        
        stock_result = {
            "stock": stock["fyers_symbol"] ,
            "updateddatetime": get_current_datetime(),
            "current_price":live_prices,
            "strategies": strategies
        }
        logger.info(f"Processed stock: {stock['fyers_symbol']}")
        return stock_result
    except Exception as e:
        logger.error(f"Error processing stock: {stock['fyers_symbol']} - {str(e)}")
        return None

async def main_abs_system(fyers, nse):
    try:
        logger.info("Starting ABS system")
        list_of_index = ["NSE:NIFTY50-INDEX","NSE:NIFTYBANK-INDEX"]


        all_sector_df = nse.getNSEIndexList()

        # STOCKS ----------------------------------------------------------------
        stocks_df = nse.getNSEStockList("NIFTY%20MIDCAP150%20MOMENTUM%2050")
        stocks_df["fyers_symbol"] = stocks_df["symbol"].apply(lambda symbol: f"NSE:{symbol}-EQ")

        # # Fetch Live Prices
        live_price_symbol_list = stocks_df["fyers_symbol"].tolist()
        live_price_symbol_list.extend(list_of_index)
        live_prices = await fyers.get_current_ltp(live_price_symbol_list)
        
        
        stock_tasks = [process_stock(stock=row,
                                     fyers=fyers,
                                     live_prices = live_prices.get(row["fyers_symbol"].split(":")[1])
                                     ,all_sector_df=all_sector_df
                                     ) for index, row in stocks_df.iterrows()]
        stock_results = await asyncio.gather(*stock_tasks)

        # INDEX Pending----------------------------------------------------------------
        index_tasks = [process_stock(
                            stock={"fyers_symbol":index_name},
                            fyers=fyers,
                            live_prices=live_prices.get(index_name.split(":")[1]),
                            all_sector_df=all_sector_df
                            ) for index_name in list_of_index]

        index_results = await asyncio.gather(*index_tasks)
        
        logger.info("Finished processing all stocks")
        save_results({"index":index_results,"stocks":stock_results,})
        logger.info("Results saved successfully")
    except Exception as e:
        logger.error(f"Error in main ABS system - {str(e)}")
