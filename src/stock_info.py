class StockInfo:
    def __init__(self):
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
