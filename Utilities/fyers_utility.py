

def convert_nse_symbol_to_fyers_symbol(symbol_list):

    return [
        f"NSE:{symbol}-EQ" if symbol not in ["NIFTY50", "NIFTYBANK"] else f"NSE:{symbol}-INDEX"
        for symbol in symbol_list
    ]