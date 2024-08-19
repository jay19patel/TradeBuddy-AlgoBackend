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

async def main():
    global fyers, nse, todays_date
    fyers = FyersHelper()
    if not await fyers.authentication():
        fyers.get_new_access_token()
    nse = TradeBuddyNSE()
    todays_date = datetime.date.today()

    await main_abs_system(fyers,nse)
    print("------------------------------------------run-------------------------------------------")


if __name__ == "__main__":
    asyncio.run(main())
