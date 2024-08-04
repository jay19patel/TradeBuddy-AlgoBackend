import requests

class TradebuddyHelper:
    def __init__(self):
        self.access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBY2NvdW50SWQiOiJXWVcwQiIsIkFjY291bnRFbWFpbCI6Imp1c3RqYXl5MTlAZ21haWwuY29tIiwiQWNjb3VudFJvbGUiOiJVc2VyIiwiZXhwIjoxNzIyODIyMjQxLCJqdGkiOiJjMDVlYWE0ZC0zODljLTQxZjItYTMzMi1jMTdhZWQ1OTEzNDcifQ.s5ryp7WPKJKiMOmH0vIPIilptc5Wxaxc5k7ysKgAxpU"
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def open_positions(self, today):
        url = 'http://127.0.0.1:8000/order/get_position'
        params = {'today': today}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_orderbook(self, today):
        url = 'http://127.0.0.1:8000/order/get_position'
        params = {'today': today}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None
