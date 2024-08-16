# from Broker.pre_processing_df import add_indicators
from Strategies.strategie_1 import apply_strategy_ema,apply_strategy_rsi
from utils import get_current_datetime,save_results
import asyncio
import logging
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def process_stock(stock, fyers):
    try:
        # historical_data = await add_indicators(fyers.Historical_Data(stock, 5))
        historical_data = None
        strategies = {
            "ema": await asyncio.create_task(apply_strategy_ema(df=historical_data, current_price=15)),
            "rsi": await asyncio.create_task(apply_strategy_rsi(df=historical_data, current_price=15)),
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
