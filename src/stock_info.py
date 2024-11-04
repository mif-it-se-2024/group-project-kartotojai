import json

class StockInfo:
    def __init__(self, stock_file='stocks.json'):
        self.stock_file = stock_file
        self.load_stocks()

    def load_stocks(self):
        with open(self.stock_file, 'r') as file:
            self.stocks = json.load(file)

    def get_stock(self, ticker):
        return self.stocks.get(ticker.upper(), None)

    def display_stocks(self):
        print("Available Stocks:")
        for ticker, info in self.stocks.items():
            print(f"{ticker}: Price: {info['price']}, Market Cap: {info.get('market_cap', 'N/A')}, Dividend Yield: {info.get('dividend_yield', 'N/A')}")
