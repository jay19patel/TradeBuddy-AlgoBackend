import logging
from TB.broker.fyers import FyersHelper
from TB.broker.tradebuddy import TradebuddyHelper
from TB.nse.base import TradeBuddyNSE
from TB.abs.for_stock import ABSStock
from TB.abs.for_index import ABSIndex
import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

fyers = None
tradebuddy = None
nse = None
abs_stock = None
abs_index = None

todays_date = None


def initialize_system():
    """
    Initializes the system by setting up database connections and instantiating necessary classes.
    """
    global fyers, tradebuddy,nse,abs_stock,abs_index,todays_date
    try:
        logging.info("Initializing system...")
        fyers = FyersHelper()
        tradebuddy = TradebuddyHelper()
        nse =TradeBuddyNSE()
        abs_stock =ABSStock(nse,fyers,tradebuddy)
        abs_index =ABSIndex(nse,fyers,tradebuddy)
        todays_date =datetime.date.today()
        logging.info("System initialized successfully.")
        return True
    except Exception as e:
        logging.error(f"Error initializing system: {str(e)}")
        return False

def execute_tradebuddy_abs():
    global fyers, tradebuddy,nse,abs_stock,abs_index,todays_date
    if fyers is None or tradebuddy is None or nse is None or abs_stock is None or abs_index is None:
        logging.error("System not initialized. Please call initialize_system() first.")
        return
    try:
        logging.info("Checking if system is up-to-date...")
        if not todays_date == datetime.date.today():
            logging.error("Objects are expired. Please re-initialize the system.")
            raise ValueError("Objects are expired. Please re-initialize the system.")
        
        logging.info("System is up-to-date.")
        
        
    except ValueError as e:
        logging.error(f"Error: {str(e)}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise

def shutdown_system():
    """
    Shuts down the system by removing class objects and closing any open connections.
    """
    global fyers, tradebuddy,nse,abs_stock,abs_index,todays_date
    try:
        logging.info("Shutting down system...")
        del fyers
        del tradebuddy
        del nse
        del abs_stock
        del abs_index
        del todays_date
        logging.info("System shut down successfully.")
    except Exception as e:
        logging.error(f"Error shutting down system: {str(e)}")
        raise