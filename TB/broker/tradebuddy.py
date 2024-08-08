import requests

class TradebuddyHelper:
    def __init__(self):
        self.access_token = ""
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def open_positions(self):
        return None

    def get_open_stoporder(self, today):
        """"Find Open STOPMARKET Orders """
        return None

    def order_buy(self):
        pass

    def order_sell(self):
        pass

    def update_order(self):
        pass
    