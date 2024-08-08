from datetime import date, datetime, timedelta
from functools import wraps
from fyers_apiv3 import fyersModel
import pandas as pd
import pytz
import time
import sys


# Custom
from TB.core.config import setting

class FyersHelper:
    def __init__(self):
        self.userid = setting.USER_ID
        self.mobileno = setting.MOBILE_NO
        self.client_id = setting.CLIENT_ID
        self.secret_key = setting.SECRET_KEY
        self.app_pin = setting.APP_PIN
        self.totp_key = setting.TOTP_KEY
        self.redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
        self.response_type = "code"
        self.grant_type = "authorization_code"
        self.state = "sample_state"
        self.authorization_expiry = None
        self.access_token = None
        self.fyers_root = None
    
    def get_auth_link(self):
        self.session = fyersModel.SessionModel(
            client_id=self.client_id,
            secret_key=self.secret_key, 
            redirect_uri=self.redirect_uri, 
            response_type=self.response_type, 
            grant_type=self.grant_type
        )
        auth_link = self.session.generate_authcode()
        print("auth_link:",auth_link)

    def generate_access_token(self):
        auth_code = input("Enter Auth code :")
        self.session.set_token(auth_code)
        response = self.session.generate_token()
        access_token = response['access_token']
        file_path = "access_token.txt"
        with open(file_path, "w") as f:
            access_token = f.write()
        print(access_token)

    def authenticate(self):
        try:
            file_path = "access_token.txt"
            with open(file_path, "r") as file:
                access_token = file.read()
                self.access_token = access_token  
            self.authorization_expiry = date.today()
            self.fyers_root = fyersModel.FyersModel(is_async=False
                                                     ,client_id=self.client_id
                                                     ,token=self.access_token)
            self.full_name = self.fyers_root.get_profile()['data']['name']
            print("Authetication sucess for:",self.full_name)
            return True
        except Exception as e:
            self.authorization_expiry = None
            print(e)
            sys.exit()

    async def Historical_Data(self,Symbol,TimeFrame):
        data = {
                    "symbol":Symbol,
                    "resolution": TimeFrame,
                    "date_format":"1",
                    "range_from":(datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d'),
                    "range_to":datetime.now().strftime('%Y-%m-%d'),
                    "cont_flag":"0"
                }
        row_data =  self.fyers_root.history(data=data)
        if row_data['s']== "ok":
            df = pd.DataFrame.from_dict(row_data['candles'])
            columns_name = ['Datetime','Open','High','Low','Close','Volume']
            df.columns = columns_name
            df['Datetime'] = pd.to_datetime(df['Datetime'], unit='s')
            df['Datetime'] = df['Datetime'].dt.tz_localize(pytz.utc).dt.tz_convert('Asia/Kolkata')
            df['Datetime'] = df['Datetime'].dt.tz_localize(None)
            return df
        else:
            return row_data['s']
        
    
    def get_current_ltp(self, option_symbol:list):
            """
            option_symbol: is a list of stocks 
            example : ['NSE:ACC-EQ', 'NSE:SBIN-EQ']
            """
            try:
                option_symbol = ",".join(option_symbol)
                data = {"symbols": option_symbol}
                data = self.fyers_root.quotes(data=data)
                if data['code'] == 200:
                    return {item['v'].get('short_name', 'Unknown'): item['v'].get('lp', 'Unknown') for item in data['d']}
                return False
            except Exception as e:
                print(f"ERROR: {e}")
                return None
