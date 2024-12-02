# Scenarios for Order Matching System Tests:
# 1. Valid BUY order with a matching SELL order.
# 2. Partial matching for BUY and SELL orders.
# 3. BUY order with no matching SELL order.
# 4. Invalid BUY order (e.g., negative quantity).
# 5. Valid SELL order with a matching BUY order.
# 6. Partial matching for SELL and BUY orders.
# 7. SELL order with no matching BUY order.
# 8. Invalid SELL order (e.g., negative quantity).
# 9. Valid STOP order triggering upon market price condition.
# 10. STOP order with an invalid stop price (e.g., negative value).
# 11. Multiple matching orders (a single order matches multiple opposing orders).
# 12. Order book prioritization based on older orders.
# 13. Verifying orders are saved correctly.


import pytest
from unittest.mock import patch
from order_execution import OrderBook
from account import AccountManager

@pytest.fixture
def order_book():
    return OrderBook()

@pytest.fixture
def account_manager():
    # Create a mock AccountManager with predefined accounts
    account_manager = AccountManager()
    account_manager.accounts = {
        "1": {"balance": 10000.0, "positions": {"AAPL": 0}},  # Buyer
        "2": {"balance": 10000.0, "positions": {"AAPL": 10}},  # Seller
    }
    return account_manager

# 1. Valid BUY order with a matching SELL order
def test_valid_buy_matching_sell(order_book, account_manager):
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '1', 'order_type': 'limit'}
    sell_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '2', 'order_type': 'limit'}
    order_book.add_order(buy_order, account_manager)
    result = order_book.add_order(sell_order, account_manager)
    assert result is True, "Matching orders should execute successfully"

# 2. Partial matching for BUY and SELL orders
def test_partial_matching_buy_sell(order_book, account_manager):
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 15, 'price': 150.0, 'account_id': '1', 'order_type': 'limit'}
    sell_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '2', 'order_type': 'limit'}
    order_book.add_order(buy_order, account_manager)
    result = order_book.add_order(sell_order, account_manager)
    assert result is True, "Partial matching should update quantities"
    remaining_buy = order_book.buy_orders["AAPL"][0]["quantity"]
    assert remaining_buy == 5, "Remaining quantity should reflect partial matching"

# 3. BUY order with no matching SELL order
def test_buy_no_matching_sell(order_book, account_manager):
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 10, 'price': 140.0, 'account_id': '1', 'order_type': 'limit'}
    result = order_book.add_order(buy_order, account_manager)
    assert result is True, "Valid buy order should be stored"

# 4. Invalid BUY order
def test_invalid_buy_order(order_book, account_manager):
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': -10, 'price': 150.0, 'account_id': '1', 'order_type': 'limit'}
    result = order_book.add_order(buy_order, account_manager)
    assert result is False, "Invalid buy order should be rejected"

# 5. Valid SELL order with a matching BUY order
def test_valid_sell_matching_buy(order_book, account_manager):
    sell_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '2', 'order_type': 'limit'}
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '1', 'order_type': 'limit'}
    order_book.add_order(sell_order, account_manager)
    result = order_book.add_order(buy_order, account_manager)
    assert result is True, "Matching orders should execute successfully"

# 6. Partial matching for SELL and BUY orders
def test_partial_matching_sell_buy(order_book, account_manager):
    sell_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 15, 'price': 150.0, 'account_id': '2', 'order_type': 'limit'}
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '1', 'order_type': 'limit'}
    order_book.add_order(sell_order, account_manager)
    result = order_book.add_order(buy_order, account_manager)
    assert result is True, "Partial matching should update quantities"
    remaining_sell = order_book.sell_orders["AAPL"][0]["quantity"]
    assert remaining_sell == 5, "Remaining quantity should reflect partial matching"

# 7. SELL order with no matching BUY order
def test_sell_no_matching_buy(order_book, account_manager):
    sell_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'price': 160.0, 'account_id': '2', 'order_type': 'limit'}
    result = order_book.add_order(sell_order, account_manager)
    assert result is True, "Valid sell order should be stored"

# 8. Invalid SELL order
def test_invalid_sell_order(order_book, account_manager):
    sell_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': -10, 'price': 150.0, 'account_id': '2', 'order_type': 'limit'}
    result = order_book.add_order(sell_order, account_manager)
    assert result is False, "Invalid sell order should be rejected"

# 9. Valid STOP order triggering
def test_valid_stop_order_trigger(order_book, account_manager):
    stop_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'stop_price': 145.0, 'account_id': '2', 'order_type': 'stop'}
    order_book.add_order(stop_order, account_manager)
    order_book.update_market_price('AAPL', 145.0)
    assert len(order_book.sell_orders["AAPL"]) > 0, "Stop order should be triggered and moved to sell queue"

# 10. STOP order with an invalid stop price
def test_invalid_stop_order(order_book, account_manager):
    stop_order = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'stop_price': -145.0, 'account_id': '2', 'order_type': 'stop'}
    result = order_book.add_order(stop_order, account_manager)
    assert result is False, "Invalid stop order should be rejected"

# 11. Multiple matching orders
def test_multiple_matching_orders(order_book, account_manager):
    buy_order = {'action': 'buy', 'ticker': 'AAPL', 'quantity': 20, 'price': 150.0, 'account_id': '1', 'order_type': 'limit'}
    sell_order_1 = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '2', 'order_type': 'limit'}
    sell_order_2 = {'action': 'sell', 'ticker': 'AAPL', 'quantity': 10, 'price': 150.0, 'account_id': '2', 'order_type': 'limit'}
    order_book.add_order(buy_order, account_manager)
    order_book.add_order(sell_order_1, account_manager)
    result = order_book.add_order(sell_order_2, account_manager)
    assert result is True, "Multiple matching should complete successfully"
    assert len(order_book.sell_orders.get("AAPL", [])) == 0, "All sell orders should be matched"

# 12. Order book prioritization based on older orders
def test_order_book_prioritization(order_book, account_manager):
    # Add an older SELL order
    old_sell_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,
        'account_id': '2',
        'order_type': 'limit',
        'timestamp': "2023-12-01 12:00:00",
    }
    order_book.add_order(old_sell_order, account_manager)

    # Add a newer SELL order
    new_sell_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,
        'account_id': '2',
        'order_type': 'limit',
        'timestamp': "2023-12-02 12:00:00",
    }
    order_book.add_order(new_sell_order, account_manager)

    # Add a BUY order that matches the price
    buy_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,
        'account_id': '1',
        'order_type': 'limit',
    }
    order_book.add_order(buy_order, account_manager)

    # Verify the older order is matched first
    assert len(order_book.sell_orders["AAPL"]) == 1, "One sell order should remain after partial match"
    remaining_order = order_book.sell_orders["AAPL"][0]
    assert remaining_order["timestamp"] == "2023-12-02 12:00:00", "Newer order should remain in the order book"

# 13. Verifying orders are saved correctly
def test_orders_are_saved_correctly(order_book, account_manager):
    # Add a BUY order
    buy_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,
        'account_id': '1',
        'order_type': 'limit',
    }
    order_book.add_order(buy_order, account_manager)

    # Add a SELL order
    sell_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,
        'account_id': '2',
        'order_type': 'limit',
    }
    order_book.add_order(sell_order, account_manager)

    # Verify orders are saved in the order book
    assert "AAPL" in order_book.buy_orders, "Buy orders should be recorded in the order book"
    assert len(order_book.buy_orders["AAPL"]) == 1, "There should be exactly one buy order for AAPL"
    assert "AAPL" in order_book.sell_orders, "Sell orders should be recorded in the order book"
    assert len(order_book.sell_orders["AAPL"]) == 1, "There should be exactly one sell order for AAPL"

    # Verify the details of the stored orders
    stored_buy_order = order_book.buy_orders["AAPL"][0]
    assert stored_buy_order["quantity"] == 10, "Buy order quantity should match"
    assert stored_buy_order["price"] == 150.0, "Buy order price should match"

    stored_sell_order = order_book.sell_orders["AAPL"][0]
    assert stored_sell_order["quantity"] == 10, "Sell order quantity should match"
    assert stored_sell_order["price"] == 150.0, "Sell order price should match"
