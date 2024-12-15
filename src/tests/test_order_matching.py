"""
Scenarios for Order Matching System Tests:
 1. Valid BUY order with a matching SELL order.
 2. Partial matching for BUY and SELL orders.
 3. BUY order with no matching SELL order.
 4. Invalid BUY order (e.g., negative quantity).
 5. Valid SELL order with a matching BUY order.
 6. Partial matching for SELL and BUY orders.
 7. SELL order with no matching BUY order.
 8. Invalid SELL order (e.g., negative quantity).
 9. Valid STOP order triggering upon market price condition.
 10. STOP order with an invalid stop price (e.g., negative value).
 11. Multiple matching orders (a single order matches multiple opposing orders).
 12. Order book prioritization based on older orders.
 13. Verifying orders are saved correctly.
 14. Detailed multiple matching orders with varying prices and quantities.
 15. Rejected BUY order due to insufficient balance.
 16. Rejected SELL order due to insufficient stock.
 17. Order cancellation.
 18. Orders with zero quantity.
 19. Matching orders with price priority.
 20. FIFO priority for orders with same price.
"""

import pytest
from order_execution import OrderBook
from account import AccountManager
from datetime import datetime, timedelta
from stock_info import StockInfo
import os

@pytest.fixture(autouse=True)
def cleanup_files():
    for f in ["unmatched_orders.json", "executed_trades.json"]:
        if os.path.exists(f):
            os.remove(f)

@pytest.fixture
def stock_info():
    return StockInfo()

@pytest.fixture
def order_book(stock_info):
    return OrderBook(stock_info)

@pytest.fixture
def account_manager():
    account_manager = AccountManager()
    account_manager.accounts = {
        "1": {"balance": 10000.0, "positions": {"AAPL": 0}},
        "2": {"balance": 10000.0, "positions": {"AAPL": 100}},  # Seller with sufficient shares
    }
    return account_manager

# 1. Valid BUY order with a matching SELL order
def test_valid_buy_matching_sell(order_book, account_manager):
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '1', 'order_type': 'limit', 'timestamp': datetime.now()}
    sell_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '2', 'order_type': 'limit', 'timestamp': datetime.now()}
    order_book.add_order(buy_order, account_manager)
    result = order_book.add_order(sell_order, account_manager)
    assert result is True
    assert len(order_book.buy_orders.get("AAPL", [])) == 0
    assert len(order_book.sell_orders.get("AAPL", [])) == 0

# 2. Partial matching for BUY and SELL orders
def test_partial_matching_buy_sell(order_book, account_manager):
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 15, 'price': 150.0, 'account_id': '1', 'order_type': 'limit', 'timestamp': datetime.now()}
    sell_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '2', 'order_type': 'limit', 'timestamp': datetime.now()}
    order_book.add_order(buy_order, account_manager)
    result = order_book.add_order(sell_order, account_manager)
    assert result is True
    remaining_buy = order_book.buy_orders["AAPL"][0]["quantity"]
    assert remaining_buy == 5

# 3. BUY order with no matching SELL order
def test_buy_no_matching_sell(order_book, account_manager):
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 10, 'price': 140.0, 'account_id': '1', 'order_type': 'limit', 'timestamp': datetime.now()}
    result = order_book.add_order(buy_order, account_manager)
    assert result is True
    assert len(order_book.buy_orders["AAPL"]) == 1

# 4. Invalid BUY order
def test_invalid_buy_order(order_book, account_manager):
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': -10, 'price': 150.0, 'account_id': '1', 'order_type': 'limit', 'timestamp': datetime.now()}
    result = order_book.add_order(buy_order, account_manager)
    assert result is False

# 5. Valid SELL order with a matching BUY order
def test_valid_sell_matching_buy(order_book, account_manager):
    sell_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '2', 'order_type': 'limit', 'timestamp': datetime.now()}
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '1', 'order_type': 'limit', 'timestamp': datetime.now()}
    order_book.add_order(sell_order, account_manager)
    result = order_book.add_order(buy_order, account_manager)
    assert result is True
    assert len(order_book.buy_orders.get("AAPL", [])) == 0
    assert len(order_book.sell_orders.get("AAPL", [])) == 0

# 6. Partial matching for SELL and BUY orders
def test_partial_matching_sell_buy(order_book, account_manager):
    sell_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 15, 'price': 150.0, 'account_id': '2', 'order_type': 'limit', 'timestamp': datetime.now()}
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '1', 'order_type': 'limit', 'timestamp': datetime.now()}
    order_book.add_order(sell_order, account_manager)
    result = order_book.add_order(buy_order, account_manager)
    assert result is True
    remaining_sell = order_book.sell_orders["AAPL"][0]["quantity"]
    assert remaining_sell == 5

# 7. SELL order with no matching BUY order
def test_sell_no_matching_buy(order_book, account_manager):
    sell_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'price': 160.0, 'account_id': '2', 'order_type': 'limit', 'timestamp': datetime.now()}
    result = order_book.add_order(sell_order, account_manager)
    assert result is True
    assert len(order_book.sell_orders["AAPL"]) == 1

# 8. Invalid SELL order
def test_invalid_sell_order(order_book, account_manager):
    sell_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': -10, 'price': 150.0, 'account_id': '2', 'order_type': 'limit', 'timestamp': datetime.now()}
    result = order_book.add_order(sell_order, account_manager)
    assert result is False

# 9. Valid STOP order triggering
def test_valid_stop_order_trigger(order_book, account_manager):
    stop_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'stop_price': 145.0, 'account_id': '2', 'order_type': 'stop_market', 'timestamp': datetime.now()}
    order_book.add_order(stop_order, account_manager)
    order_book.update_market_price('AAPL', 145.0, account_manager)
    assert len(order_book.sell_orders["AAPL"]) > 0

# 10. STOP order with an invalid stop price
def test_invalid_stop_order(order_book, account_manager):
    stop_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'stop_price': -145.0, 'account_id': '2', 'order_type': 'stop_market', 'timestamp': datetime.now()}
    result = order_book.add_order(stop_order, account_manager)
    assert result is False

# 11. Multiple matching orders
def test_multiple_matching_orders(order_book, account_manager):
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 20, 'price': 150.0, 'account_id': '1', 'order_type': 'limit', 'timestamp': datetime.now()}
    sell_order_1 = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '2', 'order_type': 'limit', 'timestamp': datetime.now()}
    sell_order_2 = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '2', 'order_type': 'limit', 'timestamp': datetime.now()}
    order_book.add_order(buy_order, account_manager)
    order_book.add_order(sell_order_1, account_manager)
    result = order_book.add_order(sell_order_2, account_manager)
    assert result is True
    assert len(order_book.sell_orders.get("AAPL", [])) == 0

# 12. Order book prioritization based on older orders
def test_order_book_prioritization(order_book, account_manager):
    old_sell_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,
        'account_id': '2',
        'order_type': 'limit',
        'timestamp': datetime.now() - timedelta(days=1),
    }
    order_book.add_order(old_sell_order, account_manager)
    new_sell_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,
        'account_id': '2',
        'order_type': 'limit',
        'timestamp': datetime.now(),
    }
    order_book.add_order(new_sell_order, account_manager)
    buy_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,
        'account_id': '1',
        'order_type': 'limit',
        'timestamp': datetime.now(),
    }
    order_book.add_order(buy_order, account_manager)
    assert len(order_book.sell_orders["AAPL"]) == 1
    remaining_order = order_book.sell_orders["AAPL"][0]
    assert remaining_order["timestamp"] > (datetime.now() - timedelta(days=1))

# 13. Verifying orders are saved correctly
def test_orders_are_saved_correctly(order_book, account_manager):
    buy_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 149.0,  # Adjusted to avoid immediate match
        'account_id': '1',
        'order_type': 'limit',
        'timestamp': datetime.now(),
    }
    order_book.add_order(buy_order, account_manager)
    sell_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,  # Adjusted to avoid immediate match
        'account_id': '2',
        'order_type': 'limit',
        'timestamp': datetime.now(),
    }
    order_book.add_order(sell_order, account_manager)
    assert "AAPL" in order_book.buy_orders
    assert len(order_book.buy_orders["AAPL"]) == 1
    assert "AAPL" in order_book.sell_orders
    assert len(order_book.sell_orders["AAPL"]) == 1
    stored_buy_order = order_book.buy_orders["AAPL"][0]
    assert stored_buy_order["quantity"] == 10
    assert stored_buy_order["price"] == 149.0
    stored_sell_order = order_book.sell_orders["AAPL"][0]
    assert stored_sell_order["quantity"] == 10
    assert stored_sell_order["price"] == 150.0

# 14. Detailed multiple matching orders with varying prices and quantities
def test_multiple_matching_orders_detailed(order_book, account_manager):
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 25, 'price': 155.0, 'account_id': '1', 'order_type': 'limit', 'timestamp': datetime.now()}
    sell_order_1 = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '2', 'order_type': 'limit', 'timestamp': datetime.now()}
    sell_order_2 = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 15, 'price': 155.0, 'account_id': '2', 'order_type': 'limit', 'timestamp': datetime.now()}
    order_book.add_order(buy_order, account_manager)
    order_book.add_order(sell_order_1, account_manager)
    remaining_buy_orders = sum(order["quantity"] for order in order_book.buy_orders.get("AAPL", []))
    assert remaining_buy_orders == 15
    result_2 = order_book.add_order(sell_order_2, account_manager)
    assert result_2 is True
    remaining_sell_orders = sum(order["quantity"] for order in order_book.sell_orders.get("AAPL", []))
    assert remaining_sell_orders == 0
    assert account_manager.accounts["1"]["positions"].get("AAPL", 0) == 25
    assert account_manager.accounts["1"]["balance"] < 10000.0
    assert account_manager.accounts["2"]["balance"] > 10000.0

# 15. Rejected BUY order due to insufficient balance
def test_buy_order_rejected_insufficient_balance(order_book, account_manager):
    account_manager.accounts["1"]["balance"] = 100.0
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '1', 'order_type': 'limit', 'timestamp': datetime.now()}
    result = order_book.add_order(buy_order, account_manager)
    assert result is False
    assert len(order_book.buy_orders.get("AAPL", [])) == 0

# 16. Rejected SELL order due to insufficient stock
def test_sell_order_rejected_insufficient_stock(order_book, account_manager):
    account_manager.accounts["2"]["positions"]["AAPL"] = 0
    sell_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '2', 'order_type': 'limit', 'timestamp': datetime.now()}
    result = order_book.add_order(sell_order, account_manager)
    assert result is False

# 17. Order cancellation
def test_order_cancellation(order_book, account_manager):
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '1', 'order_type': 'limit', 'timestamp': datetime.now()}
    order_book.add_order(buy_order, account_manager)
    order_id = order_book.buy_orders["AAPL"][0]['order_id']
    result = order_book.cancel_order('1', order_id)
    assert result is True
    assert len(order_book.buy_orders.get("AAPL", [])) == 0

# 18. Orders with zero quantity
def test_order_with_zero_quantity(order_book, account_manager):
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 0, 'price': 150.0, 'account_id': '1', 'order_type': 'limit', 'timestamp': datetime.now()}
    result = order_book.add_order(buy_order, account_manager)
    assert result is False
    sell_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 0, 'price': 150.0, 'account_id': '2', 'order_type': 'limit', 'timestamp': datetime.now()}
    result = order_book.add_order(sell_order, account_manager)
    assert result is False

# 19. Matching orders with price priority
def test_price_priority_matching(order_book, account_manager):
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 10, 'price': 155.0, 'account_id': '1', 'order_type': 'limit', 'timestamp': datetime.now()}
    sell_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '2', 'order_type': 'limit', 'timestamp': datetime.now()}
    order_book.add_order(sell_order, account_manager)
    result = order_book.add_order(buy_order, account_manager)
    assert result is True
    assert len(order_book.sell_orders.get("AAPL", [])) == 0

# 20. FIFO priority for orders with same price
def test_fifo_priority_matching(order_book, account_manager):
    sell_order_1 = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '2', 'order_type': 'limit', 'timestamp': datetime.now() - timedelta(seconds=10)}
    sell_order_2 = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '2', 'order_type': 'limit', 'timestamp': datetime.now()}
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '1', 'order_type': 'limit', 'timestamp': datetime.now()}
    order_book.add_order(sell_order_1, account_manager)
    order_book.add_order(sell_order_2, account_manager)
    result = order_book.add_order(buy_order, account_manager)

    assert result is True, "Matching should prioritize older sell order"
    remaining_sell_orders = sum(order["quantity"] for order in order_book.sell_orders.get("AAPL", []))
    assert remaining_sell_orders == 10, "Only one sell order should remain in the book"
