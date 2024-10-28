import time as time_true
import pathlib
import pandas as pd
import yfinance as yf

from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Union

from pyrobot.stock_frame import StockFrame
from pyrobot.portfolio import Portfolio
from pyrobot.trades import Trade

import json
import pytz

# Define Vilnius timezone
vilnius_tz = pytz.timezone('Europe/Vilnius')

class PyRobot:

    def __init__(self, trading_account: str = None, paper_trading: bool = True) -> None:
        # Track executed trades by symbol and order type
        self.executed_trades = {}  # {(symbol, order_type): bool}
        # Other initializations...
        self.trading_account: str = trading_account
        self.portfolio: Portfolio = None
        self.trades: Dict[str, Trade] = {}
        self.historical_prices: Dict[str, Dict] = {}
        self.stock_frame: StockFrame = None
        self.paper_trading: bool = paper_trading
        self._bar_size: str = '1m'
        self._bar_type: str = 'minute'      

    def is_market_open(self) -> bool:
        now = datetime.now(vilnius_tz)
        market_open = now.replace(hour=16, minute=30, second=0, microsecond=0)
        market_close = now.replace(hour=23, minute=0, second=0, microsecond=0)
        return market_open <= now <= market_close

    def create_portfolio(self):
        """Creates a new portfolio object."""
        self.portfolio = Portfolio(account_number=self.trading_account)
        return self.portfolio

    def create_trade(
        self,
        trade_id: str,
        enter_or_exit: str,
        long_or_short: str,
        order_type: str = 'mkt',
        price: float = 0.0,
        stop_limit_price: float = 0.0
    ) -> Trade:
        """Creates a new Trade object."""
        trade = Trade()
        trade.new_trade(
            trade_id=trade_id,
            order_type=order_type,
            enter_or_exit=enter_or_exit,
            long_or_short=long_or_short,
            price=price,
            stop_limit_price=stop_limit_price
        )
        self.trades[trade_id] = trade
        return trade

    def create_stock_frame(self, data: List[dict]) -> StockFrame:
        """Creates a StockFrame from historical prices."""
        self.stock_frame = StockFrame(data=data)
        return self.stock_frame

    def grab_current_quotes(self, symbols: List[str]) -> dict:
        """Grabs the current quotes for the specified symbols."""
        tickers = yf.Tickers(symbols)
        quotes = {}
        for symbol in symbols:
            ticker = tickers.tickers[symbol]
            data = ticker.history(period='1d', interval='15m')
            if not data.empty:
                latest_data = data.iloc[-1]
                quotes[symbol] = {
                    'symbol': symbol,
                    'price': latest_data['Close'],
                    'volume': latest_data['Volume'],
                    'datetime': latest_data.name.to_pydatetime()
                }
        return quotes

    def grab_historical_prices(
        self,
        start: datetime,
        end: datetime,
        bar_size: str = '1m',
        symbols: Optional[List[str]] = None
    ) -> dict:
        """Grabs historical prices for the specified symbols."""
        self._bar_size = bar_size
        if not symbols:
            symbols = list(self.portfolio.positions.keys())
        new_prices = []

        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start, end=end, interval=bar_size)
            data.reset_index(inplace=True)
            for index, row in data.iterrows():
                new_price_mini_dict = {
                    'symbol': symbol,
                    'open': row['Open'],
                    'high': row['High'],
                    'low': row['Low'],
                    'close': row['Close'],
                    'volume': row['Volume'],
                    'datetime': row['Datetime']
                }
                new_prices.append(new_price_mini_dict)

        self.historical_prices['aggregated'] = new_prices
        return self.historical_prices

    def get_latest_bar(self, symbols: Optional[List[str]] = None) -> List[dict]:
        if not symbols:
            symbols = list(self.portfolio.positions.keys())
        latest_prices = []

        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            try:
                data = ticker.history(period='1d', interval=self._bar_size, prepost=True)
                if not data.empty:
                    latest_data = data.iloc[-1]
                    latest_timestamp = latest_data.name
                    if latest_timestamp.tzinfo is None:
                        latest_timestamp = latest_timestamp.tz_localize('UTC')
                    new_price_mini_dict = {
                        'symbol': symbol,
                        'open': latest_data['Open'],
                        'high': latest_data['High'],
                        'low': latest_data['Low'],
                        'close': latest_data['Close'],
                        'volume': latest_data['Volume'],
                        'datetime': latest_timestamp
                    }
                    latest_prices.append(new_price_mini_dict)
                    print(f"Latest data for {symbol}: {new_price_mini_dict}")
                else:
                    print(f"No data retrieved for {symbol}.")
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
        return latest_prices

    def wait_till_next_bar(self) -> None:
        curr_bar_time = datetime.now(timezone.utc)
        next_bar_time = (curr_bar_time + timedelta(minutes=1)).replace(second=0, microsecond=0)
        time_to_wait = (next_bar_time - curr_bar_time).total_seconds()

        print("=" * 80)
        print("Pausing for the next bar")
        print("-" * 80)
        print(f"Current Time: {curr_bar_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Next Bar Time: {next_bar_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Sleeping for {time_to_wait} seconds")
        print("-" * 80)
        print('')

        time_true.sleep(time_to_wait)

    def execute_signals(self, signals: dict, trades_to_execute: dict) -> None:
        """Executes trades based on the signals provided and avoids duplicate trades."""
        buys = signals.get('buys', {})
        sells = signals.get('sells', {})

        # Process trades without indicators, avoid re-execution
        for trade_id, trade in trades_to_execute.items():
            symbol = trade.order['instrument']['symbol']
            order_type = trade.order['order_type']
            execution_key = (symbol, order_type)

            # Check if this trade type for this symbol has already been executed
            if self.executed_trades.get(execution_key):
                print(f"Skipping already executed trade: {execution_key}")
                continue
            
            # Execute the trade and log its execution
            print(f"Executing trade: {execution_key}")
            self.portfolio.set_ownership_status(symbol=symbol, ownership=True)
            self.save_orders([trade.order])

            # Mark the trade as executed
            self.executed_trades[execution_key] = True
    #add some error handling
    def save_orders(self, order_response_dict: List[dict]) -> bool:
        """Saves the order responses to a JSON file."""
        folder: pathlib.PurePath = pathlib.Path(__file__).parents[1].joinpath("data")
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
        file_path = folder.joinpath('orders.json')

        if file_path.exists():
            with open(file_path, 'r') as order_json:
                orders_list = json.load(order_json)
        else:
            orders_list = []

        orders_list.extend(order_response_dict)

        with open(file=file_path, mode='w') as order_json:
            json.dump(orders_list, order_json, indent=4)
        
        print("Order saved:", order_response_dict)
        return True

    def run(self, symbols: List[str], start_date: datetime, end_date: datetime) -> None:
        """Runs the trading robot."""
        # Create portfolio
        self.create_portfolio()

        # Add positions to portfolio
        for symbol in symbols:
            self.portfolio.add_position(
                symbol=symbol,
                quantity=0,  # Start with zero quantity
                purchase_price=0.0,
                asset_type='equity',
                purchase_date=str(datetime.now().date())
            )

        # Get historical prices
        historical_prices = self.grab_historical_prices(
            start=start_date,
            end=end_date,
            bar_size='1m',
            symbols=symbols
        )

        # Create stock frame
        stock_frame = self.create_stock_frame(data=historical_prices['aggregated'])
