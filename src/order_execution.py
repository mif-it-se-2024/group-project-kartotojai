import json
from datetime import datetime

class OrderExecution:
    def __init__(self, stock_info, account):
        self.stock_info = stock_info
        self.account = account
        self.load_orders()

    def load_orders(self):
        try:
            with open('orders.json', 'r') as file:
                self.orders = json.load(file)
        except FileNotFoundError:
            self.orders = []

    def save_orders(self):
        with open('orders.json', 'w') as file:
            json.dump(self.orders, file, indent=4)

    def place_order(self, action, ticker, quantity, order_type='market', price=None):
        ticker = ticker.upper()
        stock = self.stock_info.get_stock(ticker)
        if not stock:
            print("Invalid stock ticker.")
            return

        order = {
            'id': len(self.orders) + 1,
            'action': action,
            'ticker': ticker,
            'quantity': quantity,
            'order_type': order_type,
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'status': 'pending'
        }

        if order_type == 'market':
            self.execute_order(order, stock['price'])
        else:
            self.orders.append(order)
            self.save_orders()
            print(f"Limit/Stop order placed: {order}")

    def execute_order(self, order, execution_price):
        total_cost = execution_price * order['quantity']
        if order['action'] == 'buy':
            if self.account.balance >= total_cost:
                self.account.balance -= total_cost
                self.account.add_position(order['ticker'], order['quantity'], execution_price)
                order['status'] = 'executed'
                self.account.add_transaction(order)
                print(f"Bought {order['quantity']} shares of {order['ticker']} at {execution_price}")
            else:
                print("Insufficient balance.")
        elif order['action'] == 'sell':
            if self.account.has_position(order['ticker'], order['quantity']):
                self.account.balance += total_cost
                self.account.remove_position(order['ticker'], order['quantity'])
                order['status'] = 'executed'
                self.account.add_transaction(order)
                print(f"Sold {order['quantity']} shares of {order['ticker']} at {execution_price}")
            else:
                print("Insufficient shares to sell.")
        self.save_orders()
        self.account.save_account()

    def check_pending_orders(self):
        for order in self.orders:
            if order['status'] == 'pending':
                stock = self.stock_info.get_stock(order['ticker'])
                if order['order_type'] == 'limit':
                    if (order['action'] == 'buy' and stock['price'] <= order['price']) or \
                       (order['action'] == 'sell' and stock['price'] >= order['price']):
                        self.execute_order(order, order['price'])
                elif order['order_type'] == 'stop':
                    if (order['action'] == 'buy' and stock['price'] >= order['price']) or \
                       (order['action'] == 'sell' and stock['price'] <= order['price']):
                        self.execute_order(order, stock['price'])
