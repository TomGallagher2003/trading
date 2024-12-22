import alpaca_trade_api as tradeapi
import os
from dotenv import load_dotenv
from strategy import combined_strategy
from alpaca_trade_api.rest import TimeFrame


# Initialize the Alpaca API connection
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BASE_URL = os.getenv('BASE_URL')



api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL)


def get_balance():
    account = api.get_account()
    cash_balance = account.cash
    print(f"Cash balance: ${cash_balance}")
    return float(cash_balance)

def check_stock(symbol):
    try:
        api.get_asset(symbol)
        return True
    except:
        print(f"Stock {symbol} not found or unavailable.")
        return False

def buy_stock(symbol, amount):
    balance = get_balance()
    price = api.get_latest_trade(symbol).price

    total_cost = price * amount
    if total_cost > balance:
        print("Insufficient funds to make this purchase.")
        return

    # Place the buy order
    try:
        api.submit_order(
            symbol=symbol,
            qty=amount,
            side='buy',
            type='market',
            time_in_force='gtc'  # Good 'Til Canceled
        )
        print(f"Buy order for {amount} shares of {symbol} placed at ${price} each.")
    except Exception as e:
        print(f"Error placing buy order: {e}")

def sell_stock(symbol, amount):
    # Place the sell order
    try:
        api.submit_order(
            symbol=symbol,
            qty=amount,
            side='sell',
            type='market',
            time_in_force='gtc'  # Good 'Til Canceled
        )
        print(f"Sell order for {amount} shares of {symbol} placed.")
    except Exception as e:
        print(f"Error placing sell order: {e}")

def trade():
    good_stocks = combined_strategy(api)
    for stock in good_stocks:
        buy_stock(stock, 1)


trade()