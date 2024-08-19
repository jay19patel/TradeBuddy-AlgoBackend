import logging
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from Utilities.strategies_process_engin import main_abs_system
from Broker.fyers import FyersHelper
from Broker.nse import TradeBuddyNSE

import asyncio

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='data/tb_run.log',
    filemode='a'
)

logger = logging.getLogger(__name__)

fyers = None
nse = None
todays_date = None

async def initialize_system():
    """
    Initializes the system by setting up database connections and instantiating necessary classes.
    """
    global fyers, nse, todays_date
    try:
        logging.info("Initializing system...")
        fyers = FyersHelper()
        
        nse = TradeBuddyNSE()
        todays_date = datetime.date.today()
        logging.info("System initialized successfully.")
        return True
    except Exception as e:
        todays_date = None
        logging.error(f"Error initializing system: {str(e)}")
        return False

async def execute_tradebuddy_abs():
    global fyers, nse, todays_date
    if fyers is None and nse is None:
        logging.error("System not initialized. Please call initialize_system() first.")
        await initialize_system()
        return
    try:
        logging.info("Checking if system is up-to-date...")
        if not todays_date == datetime.date.today():
            logging.error("Objects are expired. Please re-initialize the system.")
            raise ValueError("Objects are expired. Please re-initialize the system.")
        
        logging.info("System is up-to-date.")
        await main_abs_system(fyers,nse)
        print("------------------------------------------run-------------------------------------------")
        
    except ValueError as e:
        logging.error(f"Error: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise

async def shutdown_system():
    """
    Shuts down the system by removing class objects and closing any open connections.
    """
    global fyers, nse, todays_date
    try:
        logging.info("Shutting down system...")
        del fyers
        del nse
        del todays_date
        logging.info("System shut down successfully.")
    except Exception as e:
        logging.error(f"Error shutting down system: {str(e)}")
        raise

async def main():
    scheduler = AsyncIOScheduler(timezone=timezone('Asia/Kolkata'))

    # Job 1: Initialize system at 9:00 AM, Monday to Friday
    scheduler.add_job(
        initialize_system,
        CronTrigger(day_of_week='mon-fri', hour=9, minute=0),
        id='initialize_system_job'
    )

    # Job 2: Execute tradebuddy_abs every 5 minutes from 9:15 AM to 3:15 PM, Monday to Friday
    scheduler.add_job(
        execute_tradebuddy_abs,
        CronTrigger(hour='9-15', minute='*/1'),
        id='execute_tradebuddy_abs_job'
    )

    # Job 3: Shutdown system at 3:30 PM, Monday to Friday
    scheduler.add_job(
        shutdown_system,
        CronTrigger(day_of_week='mon-fri', hour=15, minute=30),
        id='shutdown_system_job'
    )

    try:
        logger.info("Scheduler started...")
        scheduler.start()
        # Keep the scheduler running
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        logger.error("Error occurred. Shutting down scheduler...")
        scheduler.shutdown()
    finally:
        logger.info("Scheduler stopped.")

if __name__ == "__main__":
    asyncio.run(main())
