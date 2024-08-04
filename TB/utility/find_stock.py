import asyncio
import time
import pandas as pd
from typing import Dict

async def get_stocks_list() -> list:
    # Return a list of dummy stock symbols
    return ["AAPL", "GOOG", "MSFT", "AMZN", "FB"]

async def get_historical_data(stock: str) -> object:
    # Return a dummy historical data object
    data = {
        "stock": stock,
        "prices": [100, 120, 110, 130, 140]
    }
    return data

async def analyze_stock(data: object) -> str:
    # Analyze the dummy historical data and return a status
    prices = data["prices"]
    if prices[-1] > prices[-2]:
        return "BUY"
    elif prices[-1] < prices[-2]:
        return "SELL"
    else:
        return "HOLD"

async def process_stock(stock: str) -> tuple:
    """Fetches historical data and analyzes it."""
    data = await get_historical_data(stock)
    status = await analyze_stock(data)
    return stock, status

async def main_execution_for_find_stocks() -> pd.DataFrame:
    """Main function to orchestrate the parallel processing."""
    stocks = await get_stocks_list()
    results = []
    
    start_time = time.time()
    
    tasks = [process_stock(stock) for stock in stocks]
    results_list = await asyncio.gather(*tasks, return_exceptions=True)
    
    for result in results_list:
        if isinstance(result, Exception):
            print(f'Generated an exception: {result}')
        else:
            stock, status = result
            if status in ["BUY", "SELL"]:
                results.append((stock, status))
    
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
    
    df = pd.DataFrame(results, columns=['Stock', 'execution_status'])
    return df

# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     final_results = loop.run_until_complete(main())
#     print(final_results)