import requests
import json
class TradebuddyHelper:
    def __init__(self):
        self.access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBY2NvdW50SWQiOiI2WlRYOSIsIkFjY291bnRFbWFpbCI6Imp1c3RqYXl5MTlAZ21haWwuY29tIiwiQWNjb3VudFJvbGUiOiJVc2VyIiwiZXhwIjoxNzIzMTk2ODM0LCJqdGkiOiI2ODdmZDA5NS03ODg0LTRmNTQtOTA5Yy02NjBjNTdmMGJmZDIifQ.oxI7jXxPHTalb4p9rzvYMnU2-ijMlv2TDYQr8EuG9eM"
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    
    def _send_request(self, method, url, data=None):
        """ Helper method to send HTTP requests and handle responses. """
        try:
            response = requests.request(method, url, headers=self.headers, json=data)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None
    
    def open_positions(self):
        """ Retrieve open positions from the API. """
        url = "http://127.0.0.1:8001/order/positions"
        result = self._send_request("GET", url)
        if result is not None:
            print("Successfully fetched open positions.")
            return result
        return None

    def get_open_stoporder(self):
        """ Find open STOPMARKET orders for the given day. """
        url = "http://127.0.0.1:8000/order/orders?open_order=True"
        result = self._send_request("GET", url)
        if result:
            print("Successfully fetched open stop order.")
            return result
        return None

    def order_buy(self, data):
        """ Place a buy order. """
        # Implement buy order logic here
        return self._send_request("POST", "http://127.0.0.1:8001/order/buy", data)

    def order_sell(self, data):
        """ Place a sell order. """
        # Implement sell order logic here
        return self._send_request("POST", "http://127.0.0.1:8001/order/sell", data)

    def update_order(self, order_id, data):
        """ Update an existing order. """
        # Implement update order logic here
        url = f"http://127.0.0.1:8001/order/update/{order_id}"
        return self._send_request("PUT", url, data)
