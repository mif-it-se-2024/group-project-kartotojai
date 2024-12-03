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
