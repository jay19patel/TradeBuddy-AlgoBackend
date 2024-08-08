from TB.abs.for_stock import ABSIndex
from TB.broker.fyers import FyersHelper
from TB.broker.tradebuddy import TradebuddyHelper

# fyers = FyersHelper()
tb = TradebuddyHelper()
abs_index = ABSIndex(None,None,tb)
# fyers.get_auth_link()
# fyers.generate_access_token()
# fyers.authenticate()

# abs_index.check_existing_open_positions()
# abs_index.fetch_live_price_for_stocks()
abs_index.check_any_stop_order()