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

# -------------------------- START OF TESTS --------------------------

# Test 1: Full match
def test_full_match_integration(setup_resources):
    order_book, account_manager = setup_resources

    buy_order = {
        "id": 1,
        "action": "buy",
        "ticker": "AAPL",
        "quantity": 100,
        "price": 150.0,
        "account_id": "1",
        "order_type": "limit",
        "timestamp": datetime.now()
    }
    sell_order = {
        "id": 2,
        "action": "sell",
        "ticker": "AAPL",
        "quantity": 100,
        "price": 150.0,
        "account_id": "2",
        "order_type": "limit",
        "timestamp": datetime.now()
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

# Test 2: Partial match
def test_partial_match_integration(setup_resources):
    order_book, account_manager = setup_resources

    buy_order = {
        "id": 3,
        "action": "buy",
        "ticker": "AAPL",
        "quantity": 150,
        "price": 150.0,
        "account_id": "1",
        "order_type": "limit",
        "timestamp": datetime.now()
    }
    sell_order = {
        "id": 4,
        "action": "sell",
        "ticker": "AAPL",
        "quantity": 100,
        "price": 150.0,
        "account_id": "2",
        "order_type": "limit",
        "timestamp": datetime.now()
    }

    place_orders_and_match(order_book, account_manager, [buy_order, sell_order], "AAPL")
    trades = read_executed_trades_file(order_book.executed_trades_file)

    assert len(trades) == 1
    trade = trades[0]
    assert trade["quantity"] == 100
    assert trade["price"] == 150.0
    assert trade["buy_account_id"] == "1"
    assert trade["sell_account_id"] == "2"
    assert "timestamp" in trade and datetime.fromisoformat(trade["timestamp"])

# Test 3: Multiple orders
def test_multiple_orders_integration(setup_resources):
    order_book, account_manager = setup_resources

    orders = [
        {"id": 5, "action": "buy", "ticker": "AAPL", "quantity": 50, "price": 151.0, "account_id": "1", "order_type": "limit", "timestamp": datetime.now()},
        {"id": 6, "action": "buy", "ticker": "AAPL", "quantity": 50, "price": 150.0, "account_id": "1", "order_type": "limit", "timestamp": datetime.now()},
        {"id": 7, "action": "sell", "ticker": "AAPL", "quantity": 30, "price": 150.0, "account_id": "2", "order_type": "limit", "timestamp": datetime.now()},
        {"id": 8, "action": "sell", "ticker": "AAPL", "quantity": 70, "price": 150.0, "account_id": "3", "order_type": "limit", "timestamp": datetime.now()}
    ]

    place_orders_and_match(order_book, account_manager, orders, "AAPL")
    trades = read_executed_trades_file(order_book.executed_trades_file)

    assert len(trades) >= 2, "Multiple trades should be recorded for multiple matching orders."
    for trade in trades:
        assert trade["ticker"] == "AAPL"
        assert "timestamp" in trade and datetime.fromisoformat(trade["timestamp"])

# Test 4: No match
def test_no_match_integration(setup_resources):
    order_book, account_manager = setup_resources

    buy_order = {
        "id": 9,
        "action": "buy",
        "ticker": "AAPL",
        "quantity": 100,
        "price": 149.0,
        "account_id": "1",
        "order_type": "limit",
        "timestamp": datetime.now()
    }
    sell_order = {
        "id": 10,
        "action": "sell",
        "ticker": "AAPL",
        "quantity": 100,
        "price": 150.0,
        "account_id": "2",
        "order_type": "limit",
        "timestamp": datetime.now()
    }

    place_orders_and_match(order_book, account_manager, [buy_order, sell_order], "AAPL")
    trades = read_executed_trades_file(order_book.executed_trades_file)

    assert len(trades) == 0, "No trades should occur if no price overlap."

# -------------------------- END OF TESTS --------------------------
