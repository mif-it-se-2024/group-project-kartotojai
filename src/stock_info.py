class StockInfo:
    def __init__(self):
        self.stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA']

    def is_valid_ticker(self, ticker):
        return ticker in self.stocks

    def display_stocks(self):
        print("Available Stocks:")
        for stock in self.stocks:
            print(f"- {stock}")

    def display_stock_info(self, ticker, order_book):
        if not self.is_valid_ticker(ticker):
            print(f"{ticker} is not a valid ticker.")
            return
        print(f"Stock Info for {ticker}:")
        best_bid, best_ask = order_book.get_best_bid_ask(ticker)
        if best_bid is not None or best_ask is not None:
            print(f"  Best Bid (Buy Price): {best_bid if best_bid is not None else 'N/A'}")
            print(f"  Best Ask (Sell Price): {best_ask if best_ask is not None else 'N/A'}")
        else:
            print("  No orders available for this stock.")
