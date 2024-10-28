import time
from datetime import datetime, timedelta

from pyrobot.main import PyRobot

# Define the symbols you want to trade
symbols = ['AAPL']

# Initialize the trading robot
trading_robot = PyRobot(paper_trading=True)

# Create a new portfolio
trading_robot_portfolio = trading_robot.create_portfolio()

# Add positions to the portfolio
for symbol in symbols:
    trading_robot.portfolio.add_position(
        symbol=symbol,
        quantity=0,  # Start with zero quantity
        purchase_price=0.0,
        asset_type='equity',
        purchase_date=str(datetime.now().date()),
        owned=False
    )

# Define date range for historical data (optional for backtesting purposes)
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

# Fetch historical prices (if needed for backtesting, otherwise skip this part)
historical_prices = trading_robot.grab_historical_prices(
    start=start_date,
    end=end_date,
    bar_size='1m',
    symbols=symbols
)

# Create a stock frame (used to organize the data)
stock_frame = trading_robot.create_stock_frame(data=historical_prices['aggregated'])

# Create and configure simple trades (market and limit orders for both long and short positions)
for symbol in symbols:
    # # Market Order - Long Position
    # trade_long_market = trading_robot.create_trade(
    #     trade_id=f'long_market_{symbol.lower()}',
    #     enter_or_exit='enter',
    #     long_or_short='long',
    #     order_type='mkt'
    # )
    # trade_long_market.instrument(
    #     symbol=symbol,
    #     quantity=100,  # Example quantity
    #     asset_type='EQUITY'
    # )
    # trading_robot.trades[trade_long_market.trade_id] = trade_long_market

    # # Limit Order - Long Position
    # trade_long_limit = trading_robot.create_trade(
    #     trade_id=f'long_limit_{symbol.lower()}',
    #     enter_or_exit='enter',
    #     long_or_short='long',
    #     order_type='lmt',
    #     price=0.0  # Replace with desired limit price
    # )
    # trade_long_limit.instrument(
    #     symbol=symbol,
    #     quantity=100,
    #     asset_type='EQUITY'
    # )
    # trading_robot.trades[trade_long_limit.trade_id] = trade_long_limit

    # Market Order - Short Position
    trade_short_market = trading_robot.create_trade(
        trade_id=f'short_market_{symbol.lower()}',
        enter_or_exit='enter',
        long_or_short='short',
        order_type='mkt'
    )
    trade_short_market.instrument(
        symbol=symbol,
        quantity=100,
        asset_type='EQUITY'
    )
    trading_robot.trades[trade_short_market.trade_id] = trade_short_market

    # # Limit Order - Short Position
    # trade_short_limit = trading_robot.create_trade(
    #     trade_id=f'short_limit_{symbol.lower()}',
    #     enter_or_exit='enter',
    #     long_or_short='short',
    #     order_type='lmt',
    #     price=0.0  # Replace with desired limit price
    # )
    # trade_short_limit.instrument(
    #     symbol=symbol,
    #     quantity=100,
    #     asset_type='EQUITY'
    # )
    # trading_robot.trades[trade_short_limit.trade_id] = trade_short_limit

# Prepare trades dictionary for execution
trades_dict = {trade.trade_id: trade for trade in trading_robot.trades.values()}

# Start the trading loop
while True:
    if not trading_robot.is_market_open():
        print("Market is closed. Waiting for market to open...")
        time.sleep(60)
        continue

    # Grab the latest bar
    latest_bars = trading_robot.get_latest_bar(symbols=symbols)

    if not latest_bars:
        print("No new bar data available. Waiting...")
        trading_robot.wait_till_next_bar()
        continue

    # Add the new bar to the stock frame
    stock_frame.add_rows(data=latest_bars)

    # Execute trades without signals
    empty_signals = {'buys': {}, 'sells': {}}
    trading_robot.execute_signals(signals=empty_signals, trades_to_execute=trades_dict)

    # Wait till the next bar
    trading_robot.wait_till_next_bar()
