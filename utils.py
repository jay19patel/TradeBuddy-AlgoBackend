import json
from datetime import datetime
import os

def save_results(stock_results, file_path='data/stock_results.json'):
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(file_path, 'w') as f:
        json.dump(stock_results, f, indent=4)

def get_current_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
