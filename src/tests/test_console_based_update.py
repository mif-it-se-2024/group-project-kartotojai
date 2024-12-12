import pytest
from datetime import datetime
from order_execution import OrderBook
from stock_info import StockInfo
from account import AccountManager

def test_console_based_order_book_update(capsys):
    """
    Test if the order book is displayed regularly after each transaction or user command.
    """
    # Initialize StockInfo and AccountManager
    stock_info = StockInfo()
    account_manager = AccountManager()

    # Add an account with sufficient balance and positions
    account_manager.accounts = {
        "account_1": {
            "balance": 1000.0,
            "positions": {"AAPL": 10}  # Ensure enough shares for the sell order
        }
    }

    # Initialize OrderBook
    order_book = OrderBook(stock_info=stock_info)

    # Create mock orders
    buy_order = {
        "account_id": "account_1",
        "ticker": "AAPL",
        "quantity": 10,
        "price": 150.0,
        "order_type": "limit",
        "action": "buy",
        "timestamp": datetime.now()
    }

    sell_order = {
        "account_id": "account_1",
        "ticker": "AAPL",
        "quantity": 5,
        "price": 155.0,
        "order_type": "limit",
        "action": "sell",
        "timestamp": datetime.now()
    }

    # Add orders to the order book and capture outputs
    order_book.add_order(buy_order, account_manager)
    order_book.display_order_book()
    captured_buy = capsys.readouterr()

    order_book.add_order(sell_order, account_manager)
    order_book.display_order_book()
    captured_sell = capsys.readouterr()

    # Verify the order book is displayed correctly after each transaction
    assert "Order Book:" in captured_buy.out, "Order book not displayed after buy order."
    assert "Ticker: AAPL" in captured_buy.out, "Ticker not displayed after buy order."
    assert "Account account_1 wants to buy 10 at 150.0" in captured_buy.out, "Buy order not displayed."

    assert "Order Book:" in captured_sell.out, "Order book not displayed after sell order."
    assert "Ticker: AAPL" in captured_sell.out, "Ticker not displayed after sell order."
    assert "Account account_1 wants to sell 5 at 155.0" in captured_sell.out, "Sell order not displayed."
