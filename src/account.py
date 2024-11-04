import json

class Account:
    def __init__(self, account_file='account.json'):
        self.account_file = account_file
        self.load_account()

    def load_account(self):
        try:
            with open(self.account_file, 'r') as file:
                data = json.load(file)
                self.balance = data['balance']
                self.positions = data['positions']
                self.transactions = data['transactions']
        except FileNotFoundError:
            self.balance = 10000.00  # Starting balance
            self.positions = {}
            self.transactions = []

    def save_account(self):
        with open(self.account_file, 'w') as file:
            json.dump({
                'balance': self.balance,
                'positions': self.positions,
                'transactions': self.transactions
            }, file, indent=4)

    def add_position(self, ticker, quantity, price):
        if ticker in self.positions:
            total_quantity = self.positions[ticker]['quantity'] + quantity
            total_cost = (self.positions[ticker]['average_cost'] * self.positions[ticker]['quantity']) + (price * quantity)
            average_cost = total_cost / total_quantity
            self.positions[ticker]['quantity'] = total_quantity
            self.positions[ticker]['average_cost'] = average_cost
        else:
            self.positions[ticker] = {'quantity': quantity, 'average_cost': price}

    def remove_position(self, ticker, quantity):
        if ticker in self.positions and self.positions[ticker]['quantity'] >= quantity:
            self.positions[ticker]['quantity'] -= quantity
            if self.positions[ticker]['quantity'] == 0:
                del self.positions[ticker]
        else:
            print("Error removing position.")

    def has_position(self, ticker, quantity):
        return ticker in self.positions and self.positions[ticker]['quantity'] >= quantity

    def display_balance(self):
        print(f"Current Balance: {self.balance}")
        print("Current Positions:")
        for ticker, pos in self.positions.items():
            print(f"{ticker}: Quantity: {pos['quantity']}, Average Cost: {pos['average_cost']}")

    def display_transactions(self):
        print("Transaction History:")
        for txn in self.transactions:
            print(txn)

    def add_transaction(self, order):
        transaction = {
            'timestamp': order['timestamp'],
            'action': order['action'],
            'ticker': order['ticker'],
            'quantity': order['quantity'],
            'order_type': order['order_type'],
            'price': order['price'],
            'status': order['status']
        }
        self.transactions.append(transaction)
        self.save_account()
