from fyers_apiv3 import fyersModel
import asyncio
from Core.config import setting
import os
import pandas as pd
from datetime import datetime ,timedelta
import pytz
class FyersHelper(fyersModel.FyersModel):
    def __init__(self):
        self.access_token: any = None
        self.secret_key = setting.SECRET_KEY
        self.access_token_file = "access_token.txt"  # Initialize this before calling _get_access_token
        self._get_access_token()
        self.authenticated = False

        super().__init__(
            is_async=True,
            log_path=None,
            client_id=setting.CLIENT_ID,
            token=self.access_token
        )

    def _get_access_token(self):
        try:
            if os.path.exists(self.access_token_file):
                with open(self.access_token_file, "r") as f:
                    self.access_token = f.read().strip()
        except FileNotFoundError:
            print("Access token file not found")
            self.access_token = None
        except Exception as e:
            print(f"Error reading access token file: {e}")
            self.access_token = None

    async def authentication(self):
        try:
            if os.path.exists(self.access_token_file):
                with open(self.access_token_file, "r") as f:
                    self.access_token = f.read().strip()
            profile = await self.get_profile()
            if profile.get("code") == -17:
                raise Exception("Not Authorized")
            self.full_name = profile['data']['name']
            self.authenticated = True
            print(f"Successful authentication: {self.full_name}")
            return True
        except Exception as e:
            print(f"Authentication Error: {e}")
            return False
            # sys.exit(1)

    def get_new_access_token(self):
        try:
            self.session = fyersModel.SessionModel(
                client_id=self.client_id,
                secret_key=self.secret_key,
                redirect_uri="https://trade.fyers.in/api-login/redirect-uri/index.html",
                response_type="code",
                grant_type="authorization_code"
            )
            auth_link = self.session.generate_authcode()
            print("auth_link:", auth_link)
            auth_code = input("Enter Auth code: ")
            self.session.set_token(auth_code)
            response = self.session.generate_token()
            self.access_token = response['access_token']
            with open(self.access_token_file, "w") as f:
                f.write(self.access_token)
        except Exception as e:
            print(f"Error generating new access token: {e}")


    async def historical_data(self, symbol, timeframe):
        """Fetch historical data for a given symbol and timeframe."""
        data = {
            "symbol": symbol,
            "resolution": timeframe,
            "date_format": "1",
            "range_from": (datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d'),
            "range_to": datetime.now().strftime('%Y-%m-%d'),
            "cont_flag": "0"
        }
        response =  await self.history(data=data)
        if response['s'] == "ok":
            df = pd.DataFrame(response['candles'], columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df['Datetime'] = pd.to_datetime(df['Datetime'], unit='s').dt.tz_localize(pytz.utc).dt.tz_convert('Asia/Kolkata').dt.tz_localize(None)
            return df
        return None
    
    async def get_current_ltp(self, symbols):
        """Get the latest price (LTP) for a list of symbols."""
        try:
            data = {"symbols": ",".join(symbols)}
            response = await self.quotes(data=data)
            if response['code'] == 200:
                return {item['v'].get('short_name', 'Unknown'): item['v'].get('lp', 'Unknown') for item in response['d']}
            return None
        except Exception as e:
            print(f"ERROR: {e}")
            return None


# async def main():
#     try:
#         obj = FyersHelper()
#         if not await obj.authentication():
#             obj.get_new_access_token()
#         print(await obj.get_current_ltp(["NSE:POLICYBZR-EQ","NSE:HDFCBANK-EQ"]))
#         print("---")
#     except Exception as e:
#         print(f"Error in main: {e}")

# # Run the asynchronous main function
# if __name__ == "__main__":
#     asyncio.run(main())