from alpaca_trade_api.rest import TimeFrame
from datetime import datetime, timedelta
import pytz

# Timezone setup
eastern = pytz.timezone('US/Eastern')
today = datetime.now(pytz.utc).astimezone(eastern) - timedelta(days=1)
yesterday = today - timedelta(days=2)
today_str = today.strftime('%Y-%m-%d').split()[0]
yesterday_str = yesterday.strftime('%Y-%m-%d').split()[0]
back30 = today - timedelta(days=30)
back30_str = back30.strftime('%Y-%m-%d').split()[0]


# Pick stocks based on momentum
def pick_stocks_based_on_momentum(symbols, api):
    momentum_stocks = []
    for symbol in symbols:
        try:
            bars = api.get_bars(symbol, TimeFrame.Day, yesterday_str, today_str, adjustment='raw')
            close_today = bars[1].c
            close_yesterday = bars[0].c
            price_change = (close_today - close_yesterday) / close_yesterday
            if price_change > 0.02:  # If the price increased by more than 2%
                momentum_stocks.append(symbol)
        except:
            print(f"Failed to get data for {symbol}")
    return momentum_stocks


# Pick stocks based on volume
def pick_stocks_based_on_volume(symbols, api):
    volume_stocks = []
    for symbol in symbols:
        try:
            bars = api.get_bars(symbol, TimeFrame.Day, back30_str, today_str, adjustment='raw')
            avg_volume = sum(bar.v for bar in bars) / len(bars)
            last_bar = bars[-1]  # Most recent day
            volume_diff = (last_bar.v - avg_volume) / avg_volume
            if volume_diff > 0.05:  # If today's volume is higher than the average by at least 5%
                volume_stocks.append(symbol)
        except:
            print(f"Failed to get data for {symbol}")
    return volume_stocks


# Simple moving average strategy
def simple_moving_average(api, symbol, short_window=10, long_window=22):
    # Get bars for the last 'long_window' days
    try:
        bars = api.get_bars(symbol, TimeFrame.Day, back30_str, today_str, adjustment='raw')
        closes = [bar.c for bar in bars]

        # Ensure enough data is available
        if len(closes) < long_window:
            print(f"Not enough data for {symbol} to calculate moving averages.")
            return False

        # Calculate the moving averages
        short_ma = sum(closes[-short_window:]) / short_window
        long_ma = sum(closes[-long_window:]) / long_window

        # Check if the short moving average is above the long moving average
        if short_ma > long_ma:
            return True
        else:
            return False
    except:
        print(f"Failed to get moving average data for {symbol}")
        return False


# Get a watchlist of stock symbols
def get_watchlist():
    return [
        "AAPL", "TSLA", "AMZN", "MSFT", "GOOGL", "NFLX", "NVDA", "BABA", "AMD",
        "INTC", "DIS", "V", "PYPL", "MA", "UBER", "LYFT", "SNAP", "ZM", "SPOT",
        "VZ", "GOOG", "BA", "GE", "MMM", "COST", "WMT", "HD", "NKE", "KO", "PEP",
        "XOM", "CVX", "BP", "MCD", "YUM", "TGT", "LOW", "SBUX", "PG",
        "CL", "NSC", "CSX", "COP", "NEE", "TSM", "LMT", "RTX", "GS", "JPM", "C",
        "WFC", "USB", "AXP", "BK", "MS", "T", "VZ", "INTU", "MDLZ", "ABT", "JNJ"
    ]


# Combined strategy (momentum, volume, moving average)
def combined_strategy(api):
    print("Working...")

    watchlist = get_watchlist()

    # Picking momentum and volume-based stocks
    momentum_stocks = pick_stocks_based_on_momentum(watchlist, api)
    volume_stocks = pick_stocks_based_on_volume(watchlist, api)

    # Combining both lists and filtering based on moving average
    trade_candidates = list(set(momentum_stocks) | set(volume_stocks))
    print(f"Momentum and Volume Stocks: {trade_candidates}")

    # Filtering stocks based on simple moving average strategy
    selected_stocks = [stock for stock in trade_candidates if simple_moving_average(api, stock)]
    print(f"Selected Stocks for Trading: {selected_stocks}")

    return selected_stocks
