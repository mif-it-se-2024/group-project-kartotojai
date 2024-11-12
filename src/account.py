import json

class AccountManager:
    def __init__(self, account_file='accounts.json'):
        self.account_file = account_file
        self.load_accounts()

    def load_accounts(self):
        try:
            with open(self.account_file, 'r') as file:
                self.accounts = json.load(file)
        except FileNotFoundError:
            self.accounts = {}

    def save_accounts(self):
        with open(self.account_file, 'w') as file:
            json.dump(self.accounts, file, indent=4)

    def get_account(self, account_id):
        account_id = str(account_id)
        if account_id not in self.accounts:
            
            self.accounts[account_id] = {
                'balance': 10000.0,
                'positions': {}
            }
            self.save_accounts()
        return self.accounts[account_id]

    def update_account(self, account_id, account_data):
        self.accounts[str(account_id)] = account_data
        self.save_accounts()

    def display_account(self, account_id):
        account = self.get_account(account_id)
        print(f"Account {account_id}:")
        print(f"  Balance: {account['balance']}")
        print(f"  Positions: {account['positions']}")
