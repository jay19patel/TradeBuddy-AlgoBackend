import pandas as pd
from TB.utility.find_stock import main_execution_for_find_stocks

class ABSIndex:
    def __init__(self,nse,fyers,tradebuddy):
        self.trade_counts:int = 0
        self.open_positions = []
        self.live_price=None
        self.nse = nse
        self.fyers = fyers
        self.tradebuddy= tradebuddy

    def check_existing_open_positions(self):
        # positions = self.fyers.fyers_root.positions().get("netPositions") # for fyers
        positions  = self.tradebuddy.open_positions(today=True)
        if not positions:
            self.open_positions = []

        self.open_positions = [p["symbol"] for p in positions]
        print(f"Open Positions :{self.open_positions}")


    def fetch_live_price(self):
        # live_price = self.fyers.get_current_ltp(self.open_positions)
        live_price = {'ACC-EQ': 2435.3, 'SBIN-EQ': 847.85}
        self.live_price
        print(f"Live Price:{live_price}")


    def check_any_stop_order(self):
        # orderbook_data = self.fyers.fyers_root.orderbook()
        # if orderbook_data.get("s") == "ok" and len(orderbook_data.get("orderBook"))>0:
        orderbook_data = self.tradebuddy.get_orderbook(today=True)
        if orderbook_data:
            stopmarket_order = list(filter(lambda item: item.get("order_types") == "stopmarket", orderbook_data))
            print(orderbook_data)

        else:
            print("orderbook is emty")
        
        # check ke database ma koy open order che ke ni te



    
    async def auto_buy_sell(df: pd.DataFrame):
        """
        This method will automatically buy stocks based on the ABS system signals.

        :param df: A pandas DataFrame containing the stock data.
        :return: None

        ### The DataFrame 'df' must contain a column named 'execution_status' which will be used to determine the buy/sell signals for the ABS system.

        """
        for i,row in df.iterrows():
            if row['execution_status'] == 'buy':
                # Buy the stock
                pass
            elif row["execution_status"] == "sell":
                # Sell the stock
                pass
        


    async def main_abs_index(self):
        stocks_data = await main_execution_for_find_stocks()
        self.auto_buy(stocks_data)
        