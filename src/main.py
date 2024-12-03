1LTIS
1ltis
Online

toyota auris — 27/11/2024 16:53
mano uosis slaptazodi
1LTIS — 29/11/2024 11:29
damn koks balsas
alfa
top 10%
toyota auris — 29/11/2024 11:29
..
wtf
tai kuriuos man kelt reik
1LTIS — 29/11/2024 11:36
Milestone: 2024-11-18 Integration of Match and Trade Storage
Issue #11: Implement Trade Storage Mechanism

Description: Store executed trades in memory or a local file, ensuring all relevant trade details are saved persistently.
Acceptance Criteria:
All executed trades are stored reliably.
Trade storage mechanism is efficient.
Unit tests cover trade storage functionality.
Issue #12: Implement Trade Reporting Functionality

Description: Allow users to generate a summary of executed trades, with options to display it in the console or save it to a text file.
Acceptance Criteria:
Users can generate and view trade reports.
Trade reports include all relevant details.
Reports can be saved to a file.
situs man rod
toyota auris — 29/11/2024 11:38
primink
kur issues kelt
nes jei as paklausiu
jos uzmus mane
1LTIS — 29/11/2024 11:38
XD
amm
gite prie code issues yra
paspaudi new issue
toyota auris — 29/11/2024 11:39
ok radau
1LTIS — 29/11/2024 11:39
ir ikeli situs atskirai abu
jei geri atrodo
ir milestone priskirk
as sita endurinu jau visa ryta
XD
toyota auris — 29/11/2024 11:43
-.-
1LTIS — 29/11/2024 11:44
sita nusiusk
toyota auris — 29/11/2024 14:50
Image
1LTIS — Yesterday at 13:20
Image
toyota auris — Yesterday at 13:25
https://tenor.com/view/otis-pritstick-me-when-when-i-see-anton-aajn-gif-19793486
1LTIS — Yesterday at 13:43
eim prie psi pasedet?
toyota auris — Yesterday at 13:48
galesim
bet as db busy
1LTIS — Yesterday at 13:51
ka veiki>
toyota auris — Yesterday at 13:52
workin out
1LTIS — Yesterday at 13:52
alr
1LTIS — Yesterday at 15:03
lmk kai noresi
toyota auris — Yesterday at 15:17
dar turiu mama nuvezt iki serviso
so u ztruksiu
1LTIS — Yesterday at 15:59
ah ouk
1LTIS started a call that lasted 3 hours. — Yesterday at 17:17
1LTIS — Yesterday at 17:55
Image
2024-11-18 Integration of match and trade storage: Store matched trades in memory or file. Implement trade report print functionality.
Allow users to generate a summary of executed trades, with options to display it in the console or save it to a text file. Users can generate and view trade reports.
Trade reports include all relevant details.
Reports can be saved to a file.
Store executed trades in memory or a local file, ensuring all relevant trade details are saved persistently. All executed trades are stored reliably.
Trade storage mechanism is efficient.
toyota auris — Yesterday at 19:32
Analyze these files. Wait for my next commands in later prompts:
# account.py
import json

class AccountManager:
    def __init__(self, account_file='accounts.json'):
Expand
message.txt
17 KB
{
    "1": {
        "balance": 5200.0,
        "positions": {
            "AAPL": 132.0
        }
    },
    "2": {
        "balance": 14800.0,
        "positions": {
            "AAPL": 68.0
        }
    },
    "3": {
        "balance": 10000.0,
        "positions": {
            "AAPL": 100
        }
    }
}
1LTIS — Yesterday at 19:47
Welcome to the Stock Trading Simulator!
Type 'help' to see available commands.
Enter a command: sell 2 aapl 5 MARKEt 
Order added to the order book.
Enter a command: BUY 1 aapl 5 MARKEt
Order added to the order book.
Cannot match market orders for AAPL without a reference price.
Enter a command: order book
Order Book:

Ticker: AAPL
Buy Orders:
  Account 1 wants to buy 5.0 at Market
Sell Orders:
  Account 2 wants to sell 5.0 at Market
Enter a command: buy 1 aapl 3 limit 150
Order added to the order book.
Cannot match market orders for AAPL without a reference price.
Enter a command: order book
Order Book:

Ticker: AAPL
Buy Orders:
  Account 1 wants to buy 5.0 at Market
  Account 1 wants to buy 3.0 at 150.0
Sell Orders:
  Account 2 wants to sell 5.0 at Market
toyota auris — Yesterday at 22:16
def match_orders(self, ticker, account_manager):
        buy_orders = self.buy_orders.get(ticker, deque())
        sell_orders = self.sell_orders.get(ticker, deque())

        # Sort orders
        buy_orders = deque(sorted(buy_orders, key=lambda o: (
Expand
message.txt
6 KB
toyota auris — Today at 10:10
nubas
kelkis
1LTIS — Today at 10:17
yuh
toyota auris started a call. — Today at 10:17
toyota auris — Today at 11:08
class StockInfo:
    def init(self):
        self.stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA']
        self.initial_prices = {
            'AAPL': 150.0,
            'MSFT': 200.0,
            'GOOG': 2500.0,
            'AMZN': 3300.0,
            'TSLA': 700.0
        }

    def is_valid_ticker(self, ticker):
        return ticker in self.stocks

    def get_initial_price(self, ticker):
        return self.initial_prices.get(ticker)

    def display_stocks(self):
        print("Available Stocks:")
        for stock in self.stocks:
            print(f"- {stock}")

    def display_stock_info(self, ticker, order_book):
        if not self.is_valid_ticker(ticker):
            print(f"{ticker} is not a valid ticker.")
            return
        print(f"Stock Info for {ticker}:")
        last_price = order_book.last_trade_price.get(ticker, self.get_initial_price(ticker))
        print(f"  Last Trade Price: {last_price if last_price is not None else 'N/A'}")
        best_bid, best_ask = order_book.get_best_bid_ask(ticker)
        if best_bid is not None or best_ask is not None:
            print(f"  Best Bid (Buy Price): {best_bid if best_bid is not None else 'N/A'}")
            print(f"  Best Ask (Sell Price): {best_ask if best_ask is not None else 'N/A'}")
        else:
            print("  No orders available for this stock.")
from stock_info import StockInfo
from account import AccountManager
from order_execution import OrderBook
from datetime import datetime

def main():
    stock_info = StockInfo()
    account_manager = AccountManager()
    order_book = OrderBook(stock_info)  # Pass stock_info to OrderBook

    print("Welcome to the Stock Trading Simulator!")
    print("Type 'help' to see available commands.")
    while True:
        command = input("Enter a command: ").strip()
        parts = command.split()
        if not parts:
            print("Please enter a command. Type 'help' to see available commands.")
            continue

        cmd = parts[0].lower()

        if cmd == 'help':
            print("""
Available Commands:
- buy <account_id> <ticker> <quantity> [order_type] [price]
- sell <account_id> <ticker> <quantity> [order_type] [price]
- stock info [<ticker>]
- account info <account_id>
- order book
- executed trades display
- executed trades export <filename>
- exit
""")
        elif cmd == 'exit':
            print("Exiting the simulator.")
            break
        elif cmd == 'stock':
            if len(parts) >= 2 and parts[1].lower() == 'info':
                if len(parts) == 3:
                    ticker = parts[2].upper()
                    stock_info.display_stock_info(ticker, order_book)
                else:
                    stock_info.display_stocks()
            else:
                print("Invalid command. Usage: stock info [<ticker>]")
        elif cmd == 'account':
            if len(parts) == 3 and parts[1].lower() == 'info':
                account_id = parts[2]
                account_manager.display_account(account_id)
            else:
                print("Invalid command. Usage: account info <account_id>")
        elif cmd == 'order':
            if len(parts) == 2 and parts[1].lower() == 'book':
                order_book.display_order_book()
            else:
                print("Invalid command. Usage: order book")
        elif cmd == 'executed':
            if len(parts) >= 2 and parts[1].lower() == 'trades':
                if len(parts) == 3 and parts[2].lower() == 'display':
                    order_book.display_executed_trades()
                elif len(parts) == 4 and parts[2].lower() == 'export':
                    filename = parts[3]
                    order_book.export_executed_trades(filename)
                else:
                    print("Invalid command. Usage:")
                    print("  executed trades display")
                    print("  executed trades export <filename>")
            else:
                print("Invalid command. Usage:")
                print("  executed trades display")
                print("  executed trades export <filename>")
        elif cmd in ['buy', 'sell']:
            if len(parts) >= 4:
                action = cmd
                account_id = parts[1]
                ticker = parts[2].upper()
                if not stock_info.is_valid_ticker(ticker):
                    print(f"Error: {ticker} is not a valid ticker.")
                    continue
                try:
                    quantity = float(parts[3])
                    if quantity <= 0:
                        print("Error: Quantity must be a positive number.")
                        continue
                except ValueError:
                    print("Error: Quantity must be a number.")
                    continue

                order_type = 'market'
                price = None

                if len(parts) >= 5:
                    order_type = parts[4].lower()
                    if order_type not in ['market', 'limit']:
                        print("Error: Order type must be 'market' or 'limit'.")
                        continue
                if len(parts) == 6:
                    try:
                        price = float(parts[5])
                        if price <= 0:
... (40 lines left)
Collapse
message.txt
6 KB
﻿
from stock_info import StockInfo
from account import AccountManager
from order_execution import OrderBook
from datetime import datetime

def main():
    stock_info = StockInfo()
    account_manager = AccountManager()
    order_book = OrderBook(stock_info)  # Pass stock_info to OrderBook

    print("Welcome to the Stock Trading Simulator!")
    print("Type 'help' to see available commands.")
    while True:
        command = input("Enter a command: ").strip()
        parts = command.split()
        if not parts:
            print("Please enter a command. Type 'help' to see available commands.")
            continue

        cmd = parts[0].lower()

        if cmd == 'help':
            print("""
Available Commands:
- buy <account_id> <ticker> <quantity> [order_type] [price]
- sell <account_id> <ticker> <quantity> [order_type] [price]
- stock info [<ticker>]
- account info <account_id>
- order book
- executed trades display
- executed trades export <filename>
- exit
""")
        elif cmd == 'exit':
            print("Exiting the simulator.")
            break
        elif cmd == 'stock':
            if len(parts) >= 2 and parts[1].lower() == 'info':
                if len(parts) == 3:
                    ticker = parts[2].upper()
                    stock_info.display_stock_info(ticker, order_book)
                else:
                    stock_info.display_stocks()
            else:
                print("Invalid command. Usage: stock info [<ticker>]")
        elif cmd == 'account':
            if len(parts) == 3 and parts[1].lower() == 'info':
                account_id = parts[2]
                account_manager.display_account(account_id)
            else:
                print("Invalid command. Usage: account info <account_id>")
        elif cmd == 'order':
            if len(parts) == 2 and parts[1].lower() == 'book':
                order_book.display_order_book()
            else:
                print("Invalid command. Usage: order book")
        elif cmd == 'executed':
            if len(parts) >= 2 and parts[1].lower() == 'trades':
                if len(parts) == 3 and parts[2].lower() == 'display':
                    order_book.display_executed_trades()
                elif len(parts) == 4 and parts[2].lower() == 'export':
                    filename = parts[3]
                    order_book.export_executed_trades(filename)
                else:
                    print("Invalid command. Usage:")
                    print("  executed trades display")
                    print("  executed trades export <filename>")
            else:
                print("Invalid command. Usage:")
                print("  executed trades display")
                print("  executed trades export <filename>")
        elif cmd in ['buy', 'sell']:
            if len(parts) >= 4:
                action = cmd
                account_id = parts[1]
                ticker = parts[2].upper()
                if not stock_info.is_valid_ticker(ticker):
                    print(f"Error: {ticker} is not a valid ticker.")
                    continue
                try:
                    quantity = float(parts[3])
                    if quantity <= 0:
                        print("Error: Quantity must be a positive number.")
                        continue
                except ValueError:
                    print("Error: Quantity must be a number.")
                    continue

                order_type = 'market'
                price = None

                if len(parts) >= 5:
                    order_type = parts[4].lower()
                    if order_type not in ['market', 'limit']:
                        print("Error: Order type must be 'market' or 'limit'.")
                        continue
                if len(parts) == 6:
                    try:
                        price = float(parts[5])
                        if price <= 0:
                            print("Error: Price must be a positive number.")
                            continue
                    except ValueError:
                        print("Error: Price must be a number.")
                        continue

                # Create order
                order = {
                    'action': action,
                    'account_id': account_id,
                    'ticker': ticker,
                    'quantity': quantity,
                    'order_type': order_type,
                    'price': price,
                    'timestamp': datetime.now()
                }

                # Validate order
                if order_type == 'limit' and price is None:
                    print("Error: Limit orders require a price.")
                    continue
                if order_type == 'market' and price is not None:
                    print("Error: Market orders should not have a price.")
                    continue

                # Add order to order book
                order_added = order_book.add_order(order, account_manager)
                if not order_added:
                    continue  # Skip to the next command

                # Attempt to match orders immediately
                order_book.match_orders(ticker, account_manager)
            else:
                print("Invalid command. Usage: buy/sell <account_id> <ticker> <quantity> [order_type] [price]")
        else:
            print("Unknown command. Type 'help' to see available commands.")

if __name__ == '__main__':
    main()
message.txt
6 KB
