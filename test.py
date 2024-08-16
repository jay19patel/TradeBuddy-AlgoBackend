import asyncio
from app import main_abs_system
from Broker import fyers,nse




asyncio.run(main_abs_system(None,nse.TradeBuddyNSE()))