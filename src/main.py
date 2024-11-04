from stock_info import StockInfo
from order_execution import OrderExecution
from account import Account

def main():
    stock_info = StockInfo()
    account = Account()
    order_execution = OrderExecution(stock_info, account)

    while True:
        command = input("Enter a command (type 'help' for options): ").strip().lower()
        if command == 'help':
            print("""
Available Commands:
- buy <ticker> <quantity> [order_type] [price]
- sell <ticker> <quantity> [order_type] [price]
- stock info
- check_balance
- show_orders
- cancel_order <order_id>
- exit
""")
        elif command.startswith('buy'):
            args = command.split()
            if len(args) >= 3:
                ticker = args[1]
                quantity = int(args[2])
                if len(args) == 3:
                    order_execution.place_order('buy', ticker, quantity)
                elif len(args) >= 4:
                    order_type = args[3]
                    price = float(args[4]) if len(args) == 5 else None
                    order_execution.place_order('buy', ticker, quantity, order_type, price)
            else:
                print("Invalid buy command.")
        elif command.startswith('sell'):
            args = command.split()
            if len(args) >= 3:
                ticker = args[1]
                quantity = int(args[2])
                if len(args) == 3:
                    order_execution.place_order('sell', ticker, quantity)
                elif len(args) >= 4:
                    order_type = args[3]
                    price = float(args[4]) if len(args) == 5 else None
                    order_execution.place_order('sell', ticker, quantity, order_type, price)
            else:
                print("Invalid sell command.")
        elif command == 'stock info':
            stock_info.display_stocks()
        elif command == 'check_balance':
            account.display_balance()
        elif command == 'show_orders':
            print("Active Orders:")
            for order in order_execution.orders:
                print(order)
        elif command.startswith('cancel_order'):
            args = command.split()
            if len(args) == 2:
                order_id = int(args[1])
                order_execution.cancel_order(order_id)
            else:
                print("Invalid cancel_order command.")
        elif command == 'exit':
            print("Exiting.")
            break
        else:
            print("Unknown command.")

        # Check pending orders after each command
        order_execution.check_pending_orders()

if __name__ == '__main__':
    main()
