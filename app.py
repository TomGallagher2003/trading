from trading import trade
import alpaca_trade_api as tradeapi
import os
from dotenv import load_dotenv


# Initialize the Alpaca API connection
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BASE_URL = os.getenv('BASE_URL')
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL)
UNIT_SIZE = 1000


trade(api, UNIT_SIZE)

