import alpaca_trade_api as tradeapi
import os
from dotenv import load_dotenv
from strategy import combined_strategy
import math


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

def buy_stock_with_stop_loss_and_take_profit(symbol, total_cost):
    balance = get_balance()
    price = api.get_latest_trade(symbol).price
    amount = round(total_cost / price)
    if total_cost > balance:
        print("Insufficient funds to make this purchase.")
        return

    # Calculate stop loss and take profit prices
    stop_loss_price = round(price * 0.98, 2)  # 2% below the purchase price
    take_profit_price = round(price * 1.05, 2)  # 5% above the purchase price

    # Place the bracket order
    try:
        api.submit_order(
            symbol=symbol,
            qty=amount,
            side='buy',
            type='market',
            time_in_force='gtc',
            order_class='bracket',
            take_profit={
                'limit_price': take_profit_price  # Set take-profit price
            },
            stop_loss={
                'stop_price': stop_loss_price  # Set stop-loss price
            }
        )
        print(f"Buy order for {amount} shares of {symbol} placed at ${price} each.")
        print(f"Take profit set at ${take_profit_price}.")
        print(f"Stop loss set at ${stop_loss_price}.")
    except Exception as e:
        print(f"Error placing buy order with stop loss and take profit: {e}")


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


def trade(api, unit):

    positions = api.list_positions()
    good_stocks = combined_strategy(api, positions)
    for stock in good_stocks:
        buy_stock_with_stop_loss_and_take_profit(stock[0], stock[1] * unit)

