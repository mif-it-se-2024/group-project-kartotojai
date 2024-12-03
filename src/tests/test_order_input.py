import pytest
from order_execution import OrderBook
from account import AccountManager

@pytest.fixture
def order_book():
    return OrderBook()

@pytest.fixture
def account_manager():
    # Mock AccountManager
    account_manager = AccountManager()
    account_manager.accounts = {
        "1": {"balance": 10000.0, "positions": {"AAPL": 10}},  # Account 1
        "2": {"balance": 15000.0, "positions": {"MSFT": 5}}   # Account 2
    }
    return account_manager

"""
Valid Order Input Tests for Order Matching System:

1. Test adding a valid `limit` buy order.
2. Test adding a valid `limit` sell order.
3. Test adding a valid `market` buy order.
4. Test adding a valid `market` sell order.
5. Test adding a valid `stop` buy order.
6. Test adding a valid `stop` sell order.
"""

# 1. Valid limit buy order
def test_valid_limit_buy_order(order_book, account_manager):
    buy_order = {
        'action': 'buy',
        'account_id': '1',
        'ticker': 'AAPL',
        'quantity': 5,
        'order_type': 'limit',
        'price': 150.0
    }
    initial_buy_orders = len(order_book.buy_orders)
    result = order_book.add_order(buy_order, account_manager)

    # Assert return value and order book state
    assert result is True, "Valid limit buy order should return True"
    assert len(order_book.buy_orders) == initial_buy_orders + 1, "OrderBook should have one more buy order"
    assert order_book.buy_orders[-1] == buy_order, "The added order should match the input order"

# 2. Valid limit sell order
def test_valid_limit_sell_order(order_book, account_manager):
    sell_order = {
        'action': 'sell',
        'account_id': '1',
        'ticker': 'AAPL',
        'quantity': 5,
        'order_type': 'limit',
        'price': 155.0
    }
    initial_sell_orders = len(order_book.sell_orders)
    result = order_book.add_order(sell_order, account_manager)

    # Assert return value and order book state
    assert result is True, "Valid limit sell order should return True"
    assert len(order_book.sell_orders) == initial_sell_orders + 1, "OrderBook should have one more sell order"
    assert order_book.sell_orders[-1] == sell_order, "The added order should match the input order"

# 3. Valid market buy order
def test_valid_market_buy_order(order_book, account_manager):
    market_buy_order = {
        'action': 'buy',
        'account_id': '1',
        'ticker': 'AAPL',
        'quantity': 10,
        'order_type': 'market'
    }
    initial_buy_orders = len(order_book.buy_orders)
    result = order_book.add_order(market_buy_order, account_manager)

    # Assert return value and order book state
    assert result is True, "Valid market buy order should return True"
    assert len(order_book.buy_orders) == initial_buy_orders + 1, "OrderBook should have one more buy order"
    assert order_book.buy_orders[-1] == market_buy_order, "The added order should match the input order"

# 4. Valid market sell order
def test_valid_market_sell_order(order_book, account_manager):
    market_sell_order = {
        'action': 'sell',
        'account_id': '1',
        'ticker': 'AAPL',
        'quantity': 5,
        'order_type': 'market'
    }
    initial_sell_orders = len(order_book.sell_orders)
    result = order_book.add_order(market_sell_order, account_manager)

    # Assert return value and order book state
    assert result is True, "Valid market sell order should return True"
    assert len(order_book.sell_orders) == initial_sell_orders + 1, "OrderBook should have one more sell order"
    assert order_book.sell_orders[-1] == market_sell_order, "The added order should match the input order"

# 5. Valid stop sell order
def test_valid_stop_sell_order(order_book, account_manager):
    stop_sell_order = {
        'action': 'sell',
        'account_id': '1',
        'ticker': 'AAPL',
        'quantity': 10,
        'order_type': 'stop',
        'stop_price': 145.0
    }
    initial_sell_orders = len(order_book.sell_orders)
    result = order_book.add_order(stop_sell_order, account_manager)

    # Assert return value and order book state
    assert result is True, "Valid stop sell order should return True"
    assert len(order_book.sell_orders) == initial_sell_orders + 1, "OrderBook should have one more stop order"
    assert order_book.sell_orders[-1] == stop_sell_order, "The added order should match the input order"

"""
Invalid Order Input Tests for Order Matching System:

1. Test adding an order with an invalid `order_type`.
2. Test adding an order with a negative `quantity`.
3. Test adding a `limit` order with a negative `price`.
4. Test adding a `limit` order with a missing `price`.
5. Test adding a `stop` order with a missing `stop_price`.
6. Test adding an order with an invalid `ticker`.
7. Test adding a `buy` order with insufficient balance.
"""

# 1. Invalid order type
def test_invalid_order_type(order_book, account_manager):
    invalid_order = {
        'action': 'buy',
        'account_id': '1',
        'ticker': 'AAPL',
        'quantity': 10,
        'order_type': 'invalid_type',  # Invalid type
        'price': 150.0
    }
    result = order_book.add_order(invalid_order, account_manager)
    assert result is False, "Order with an invalid order_type should be rejected."

# 2. Negative quantity
def test_negative_quantity(order_book, account_manager):
    invalid_order = {
        'action': 'buy',
        'account_id': '1',
        'ticker': 'AAPL',
        'quantity': -5,  # Invalid quantity
        'order_type': 'limit',
        'price': 150.0
    }
    result = order_book.add_order(invalid_order, account_manager)
    assert result is False, "Order with negative quantity should be rejected."

# 3. Negative price for limit order
def test_negative_price(order_book, account_manager):
    invalid_order = {
        'action': 'buy',
        'account_id': '1',
        'ticker': 'AAPL',
        'quantity': 10,
        'order_type': 'limit',
        'price': -150.0  # Invalid price
    }
    result = order_book.add_order(invalid_order, account_manager)
    assert result is False, "Limit order with a negative price should be rejected."

# 4. Missing price for limit order
def test_missing_price(order_book, account_manager):
    invalid_order = {
        'action': 'buy',
        'account_id': '1',
        'ticker': 'AAPL',
        'quantity': 10,
        'order_type': 'limit',  # Missing price
    }
    result = order_book.add_order(invalid_order, account_manager)
    assert result is False, "Limit order without a price should be rejected."

# 5. Missing stop price for stop order
def test_missing_stop_price(order_book, account_manager):
    invalid_order = {
        'action': 'sell',
        'account_id': '1',
        'ticker': 'AAPL',
        'quantity': 10,
        'order_type': 'stop'  # Missing stop price
    }
    result = order_book.add_order(invalid_order, account_manager)
    assert result is False, "Stop order without a stop price should be rejected."

# 6. Invalid ticker
def test_invalid_ticker(order_book, account_manager):
    invalid_order = {
        'action': 'buy',
        'account_id': '1',
        'ticker': 'INVALID',  # Invalid ticker
        'quantity': 10,
        'order_type': 'limit',
        'price': 150.0
    }
    result = order_book.add_order(invalid_order, account_manager)
    assert result is False, "Order with an invalid ticker should be rejected."

# 7. Insufficient balance for buy order
def test_insufficient_balance(order_book, account_manager):
    invalid_order = {
        'action': 'buy',
        'account_id': '1',
        'ticker': 'AAPL',
        'quantity': 10,
        'order_type': 'limit',
        'price': 200.0  # Exceeds account balance
    }
    result = order_book.add_order(invalid_order, account_manager)
    assert result is False, "Order with insufficient balance should be rejected."





