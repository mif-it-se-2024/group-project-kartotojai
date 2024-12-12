from stock_info import StockInfo
from account import AccountManager
from order_execution import OrderBook
from datetime import datetime
import os
import json

def main():
    stock_info = StockInfo()
    account_manager = AccountManager()
    order_book = OrderBook(stock_info)  # Pass stock_info to OrderBook

    print("Welcome to the Stock Trading Simulator!")
    print("Type 'help' to see available commands.")

    # Predefined default accounts configuration for resetting:
    default_accounts = {
        "1": {
            "balance": 50000.0,
            "positions": {
                "AAPL": 200,
                "TSLA": 200,
                "GOOG": 200,
                "AMZN": 200,
                "MSFT": 200
            }
        },
        "2": {
            "balance": 50000.0,
            "positions": {
                "AAPL": 200,
                "TSLA": 200,
                "GOOG": 200,
                "AMZN": 200,
                "MSFT": 200
            }
        },
        "3": {
            "balance": 50000.0,
            "positions": {
                "AAPL": 200,
                "TSLA": 200,
                "GOOG": 200,
                "AMZN": 200,
                "MSFT": 200
            }
        },
        "999": {
            "balance": 50000.0,
            "positions": {
                "AAPL": 200,
                "TSLA": 200,
                "GOOG": 200,
                "AMZN": 200,
                "MSFT": 200
            }
        }
    }

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
- stop buy <account_id> <ticker> <quantity> market <stop_price>
- stop sell <account_id> <ticker> <quantity> market <stop_price>
- stop buy <account_id> <ticker> <quantity> limit <stop_price> <limit_price>
- stop sell <account_id> <ticker> <quantity> limit <stop_price> <limit_price>
- cancel <account_id> <order_id>
- cancel stop <account_id> <order_id>
- stock info [<ticker>]
- account info <account_id>
- order book
- order stop book
- executed trades display
- executed trades export <filename>
- executed trades delete <trade_id>
- clear all
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
            elif len(parts) == 3 and parts[1].lower() == 'stop' and parts[2].lower() == 'book':
                order_book.display_stop_orders()
            else:
                print("Invalid command. Usage:")
                print("  order book")
                print("  order stop book")
        elif cmd == 'executed':
            if len(parts) >= 2 and parts[1].lower() == 'trades':
                if len(parts) == 3 and parts[2].lower() == 'display':
                    order_book.display_executed_trades()
                elif len(parts) == 4 and parts[2].lower() == 'export':
                    filename = parts[3]
                    order_book.export_executed_trades(filename)
                elif len(parts) == 4 and parts[2].lower() == 'delete':
                    trade_id = parts[3]
                    order_book.delete_executed_trade(trade_id, account_manager)
                else:
                    print("Invalid command. Usage:")
                    print("  executed trades display")
                    print("  executed trades export <filename>")
                    print("  executed trades delete <trade_id>")
            else:
                print("Invalid command. Usage:")
                print("  executed trades display")
                print("  executed trades export <filename>")
                print("  executed trades delete <trade_id>")
        elif cmd == 'cancel':
            if len(parts) == 3:
                account_id = parts[1]
                order_id = parts[2]
                order_book.cancel_order(account_id, order_id)
            elif len(parts) == 4 and parts[1].lower() == 'stop':
                account_id = parts[2]
                order_id = parts[3]
                order_book.cancel_stop_order(account_id, order_id)
            else:
                print("Invalid command. Usage:")
                print("  cancel <account_id> <order_id>")
                print("  cancel stop <account_id> <order_id>")
        elif cmd == 'stop':
            if len(parts) >= 6:
                action = parts[1].lower()
                if action not in ['buy', 'sell']:
                    print("Error: Action must be 'buy' or 'sell'.")
                    continue
                account_id = parts[2]
                ticker = parts[3].upper()
                if not stock_info.is_valid_ticker(ticker):
                    print(f"Error: {ticker} is not a valid ticker.")
                    continue
                try:
                    quantity = float(parts[4])
                    if quantity <= 0:
                        print("Error: Quantity must be positive.")
                        continue
                except ValueError:
                    print("Error: Quantity must be a number.")
                    continue
                order_subtype = parts[5].lower()
                if order_subtype == 'market':
                    if len(parts) == 7:
                        try:
                            stop_price = float(parts[6])
                            if stop_price <= 0:
                                print("Error: Stop price must be positive.")
                                continue
                        except ValueError:
                            print("Error: Stop price must be a number.")
                            continue
                        order_type = 'stop_market'
                        price = None
                    else:
                        print("Usage: stop buy/sell <account_id> <ticker> <quantity> market <stop_price>")
                        continue
                elif order_subtype == 'limit':
                    if len(parts) == 8:
                        try:
                            stop_price = float(parts[6])
                            limit_price = float(parts[7])
                            if stop_price <= 0 or limit_price <= 0:
                                print("Error: Prices must be positive.")
                                continue
                        except ValueError:
                            print("Error: Prices must be numbers.")
                            continue
                        order_type = 'stop_limit'
                        price = limit_price
                    else:
                        print("Usage: stop buy/sell <account_id> <ticker> <quantity> limit <stop_price> <limit_price>")
                        continue
                else:
                    print("Error: Order type must be 'market' or 'limit'.")
                    continue
                # Create stop order
                order = {
                    'action': action,
                    'account_id': account_id,
                    'ticker': ticker,
                    'quantity': quantity,
                    'order_type': order_type,
                    'price': price,  # For stop_limit orders
                    'stop_price': stop_price if order_type.startswith('stop') else None,
                    'timestamp': datetime.now()
                }
                # Assign unique order_id
                order_id = f"{order['account_id']}_{ticker}_{int(order['timestamp'].timestamp())}"
                order['order_id'] = order_id
                # Add order to order book
                order_added = order_book.add_order(order, account_manager)
                if not order_added:
                    continue
            else:
                print("Invalid command. Usage:")
                print("  stop buy/sell <account_id> <ticker> <quantity> market <stop_price>")
                print("  stop buy/sell <account_id> <ticker> <quantity> limit <stop_price> <limit_price>")
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
        elif cmd == 'clear':
            if len(parts) == 2 and parts[1].lower() == 'all':
                # Remove unmatched_orders and executed_trades files
                if os.path.exists(order_book.unmatched_orders_file):
                    os.remove(order_book.unmatched_orders_file)
                if os.path.exists(order_book.executed_trades_file):
                    os.remove(order_book.executed_trades_file)

                # Reset in-memory order books
                order_book.buy_orders = {}
                order_book.sell_orders = {}
                order_book.stop_buy_orders = {}
                order_book.stop_sell_orders = {}
                order_book.last_trade_price = {}

                # Reset accounts.json to default configuration
                accounts_file = account_manager.account_file
                with open(accounts_file, 'w') as f:
                    json.dump(default_accounts, f, indent=4)
                account_manager.load_accounts()

                print("All trades cleared and accounts reset to default!")
            else:
                print("Invalid command. Usage: clear all")
        else:
            print("Unknown command. Type 'help' to see available commands.")

if __name__ == '__main__':
    main()
