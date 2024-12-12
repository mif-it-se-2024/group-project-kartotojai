"""
Scenarios for Integration of Match and Trade Storage Tests:
1. Test a full match scenario: One BUY and one SELL order at the same price and quantity.
2. Test a partial match scenario: A BUY order larger than the SELL order results in a partial fill,
and only one trade should be recorded with the SELL quantity.
3. Test multiple orders on both sides: We place multiple BUY and SELL orders and ensure 
that multiple trades are recorded, reflecting the correct matching logic and storage.
4. Test a scenario where no trade occurs because prices do not overlap.
"""
import pytest
import json
import os
from datetime import datetime
from order_execution import OrderBook
from stock_info import StockInfo
from account import AccountManager

def initialize_order_book_and_account_manager():
    stock_info = StockInfo()
    account_manager = AccountManager()
    order_book = OrderBook(stock_info)
    return order_book, account_manager

@pytest.fixture
def setup_resources():
    order_book, account_manager = initialize_order_book_and_account_manager()
    # Clean up before test
    if os.path.exists(order_book.executed_trades_file):
        with open(order_book.executed_trades_file, 'w') as file:
            json.dump([], file)
    yield order_book, account_manager
    # Clean up after test
    if os.path.exists(order_book.executed_trades_file):
        os.remove(order_book.executed_trades_file)

def read_executed_trades_file(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def place_orders_and_match(order_book, account_manager, orders, ticker):
    for order in orders:
        order_book.add_order(order, account_manager)
    order_book.match_orders(ticker, account_manager)


# 1. Test a full match scenario: One BUY and one SELL order at the same price and quantity.
def test_full_match_integration(setup_resources):
    order_book, account_manager = setup_resources

    buy_order = {
        "id": 1, "type": "BUY", "ticker": "AAPL", "quantity": 100,
        "price": 150.0, "account_id": "1"
    }
    sell_order = {
        "id": 2, "type": "SELL", "ticker": "AAPL", "quantity": 100,
        "price": 150.0, "account_id": "2"
    }

    place_orders_and_match(order_book, account_manager, [buy_order, sell_order], "AAPL")
    trades = read_executed_trades_file(order_book.executed_trades_file)

    assert len(trades) == 1, "Exactly one trade should result from a perfect full match."
    trade = trades[0]
    assert trade["ticker"] == "AAPL"
    assert trade["price"] == 150.0
    assert trade["quantity"] == 100
    assert trade["buy_account_id"] == "1"
    assert trade["sell_account_id"] == "2"
    assert "timestamp" in trade and datetime.fromisoformat(trade["timestamp"])

# 2. Test a partial match scenario: A BUY order larger than the SELL order results in a partial fill,
# and only one trade should be recorded with the SELL quantity.
def test_partial_match_integration(setup_resources):
    order_book, account_manager = setup_resources

    buy_order = {
        "id": 3, "type": "BUY", "ticker": "AAPL", "quantity": 150,
        "price": 150.0, "account_id": "1"
    }
    sell_order = {
        "id": 4, "type": "SELL", "ticker": "AAPL", "quantity": 100,
        "price": 150.0, "account_id": "2"
    }

    place_orders_and_match(order_book, account_manager, [buy_order, sell_order], "AAPL")
    trades = read_executed_trades_file(order_book.executed_trades_file)

    # Only 100 shares should match
    assert len(trades) == 1
    trade = trades[0]
    assert trade["quantity"] == 100
    assert trade["price"] == 150.0
    assert trade["buy_account_id"] == "1"
    assert trade["sell_account_id"] == "2"
    assert "timestamp" in trade and datetime.fromisoformat(trade["timestamp"])

# 3. Test multiple orders on both sides: We place multiple BUY and SELL orders and ensure 
# that multiple trades are recorded, reflecting the correct matching logic and storage.
def test_multiple_orders_integration(setup_resources):
    order_book, account_manager = setup_resources

    orders = [
        {"id": 5, "type": "BUY", "ticker": "AAPL", "quantity": 50, "price": 151.0, "account_id": "1"},
        {"id": 6, "type": "BUY", "ticker": "AAPL", "quantity": 50, "price": 150.0, "account_id": "1"},
        {"id": 7, "type": "SELL", "ticker": "AAPL", "quantity": 30, "price": 150.0, "account_id": "2"},
        {"id": 8, "type": "SELL", "ticker": "AAPL", "quantity": 70, "price": 150.0, "account_id": "3"}
    ]

    # In this scenario, the orders at or crossing the price level should generate multiple trades.
    place_orders_and_match(order_book, account_manager, orders, "AAPL")
    trades = read_executed_trades_file(order_book.executed_trades_file)

    # We expect at least two trades because we have multiple matching pairs.
    assert len(trades) >= 2, "Multiple trades should be recorded for multiple matching orders."
    for trade in trades:
        assert trade["ticker"] == "AAPL"
        assert "timestamp" in trade and datetime.fromisoformat(trade["timestamp"])
        # We do not check exact match details here as it's an integration test,
        # but you can verify that all trades have the correct fields populated.

# 4. Test a scenario where no trade occurs because prices do not overlap.
def test_no_match_integration(setup_resources):
    order_book, account_manager = setup_resources

    buy_order = {
        "id": 9, "type": "BUY", "ticker": "AAPL", "quantity": 100,
        "price": 149.0, "account_id": "1"
    }
    sell_order = {
        "id": 10, "type": "SELL", "ticker": "AAPL", "quantity": 100,
        "price": 150.0, "account_id": "2"
    }

    place_orders_and_match(order_book, account_manager, [buy_order, sell_order], "AAPL")
    trades = read_executed_trades_file(order_book.executed_trades_file)

    assert len(trades) == 0, "No trades should occur if no price overlap."
