# Scenarios for Order Input Validation Tests:
# 1. Valid order input for BUY action.
# 2. Valid order input for SELL action.
# 3. Order with missing required fields (e.g., missing 'ticker').
# 4. Order with invalid data types (e.g., 'quantity' as string).
# 5. Order with negative 'quantity'.
# 6. Order with zero 'quantity'.
# 7. Order with negative 'price'.
# 8. Order with zero 'price' (for limit orders).
# 9. Order with unsupported 'order_type'.
# 10. Order with missing 'action' field.
# 11. Order with invalid 'action' value.
# 12. Order with future 'timestamp'.
# 13. Order with invalid 'ticker' symbol.
# 14. Order with extra unexpected fields.
# 15. Order with 'stop_price' in limit order.
# 16. Stop order with missing 'stop_price'.
# 17. Market order with 'price' field provided.
# 18. Valid market order input.
# 19. Valid stop order input.
# 20. Order with invalid 'account_id'.
# 21. Order with insufficient balance (for BUY orders).
# 22. Order with insufficient holdings (for SELL orders).
# 23. Order with non-existent 'account_id'.
# 24. Order with 'quantity' as float instead of integer.
# 25. Order with 'price' as string.
# 26. Order with 'quantity' as zero.
# 27. Order with 'price' as zero in limit order.
# 28. Order with 'ticker' as empty string.
# 29. Order with 'timestamp' missing.
# 30. Order with 'account_id' missing.
# 31. Order with negative 'stop_price' in stop order.
# 32. Order with invalid 'order_type' value.
# 33. Order with extremely large 'quantity' value.
# 34. Order with extremely large 'price' value.
# 35. Order with 'action' as mixed case (e.g., 'Buy').

import pytest
from unittest.mock import patch
from order_execution import OrderBook
from account import AccountManager
from datetime import datetime, timedelta
from stock_info import StockInfo

@pytest.fixture
def account_manager():
    # Create a mock AccountManager with predefined accounts
    account_manager = AccountManager()
    account_manager.accounts = {
        "1": {"balance": 10000.0, "positions": {"AAPL": 0}},
        "2": {"balance": 5000.0, "positions": {"AAPL": 20}},
    }
    return account_manager

@pytest.fixture
def stock_info():
    return StockInfo()

@pytest.fixture
def order_book(stock_info):
    return OrderBook(stock_info)
    
# Checking to see if the stock info is initializing
def test_stock_info_initialization():
    stock_info = StockInfo()
    assert stock_info is not None, "StockInfo should initialize without errors"

# 1. Valid order input for BUY action
def test_valid_buy_order_input(order_book, account_manager):
    buy_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,
        'account_id': '1',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(buy_order, account_manager)
    assert result is True, "Valid BUY order input should be accepted"

# 2. Valid order input for SELL action
def test_valid_sell_order_input(order_book, account_manager):
    sell_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 5,
        'price': 155.0,
        'account_id': '2',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(sell_order, account_manager)
    assert result is True, "Valid SELL order input should be accepted"

# 3. Order with missing required fields
def test_order_missing_required_fields(order_book, account_manager):
    incomplete_order = {
        'action': 'buy',
        # Missing 'ticker', 'quantity', 'price', etc.
        'account_id': '1',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(incomplete_order, account_manager)
    assert result is False, "Order missing required fields should be rejected"

# 4. Order with invalid data types
def test_order_invalid_data_types(order_book, account_manager):
    invalid_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 'ten',  # Invalid data type
        'price': 'one fifty',  # Invalid data type
        'account_id': '1',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(invalid_order, account_manager)
    assert result is False, "Order with invalid data types should be rejected"

# 5. Order with negative 'quantity'
def test_order_negative_quantity(order_book, account_manager):
    negative_quantity_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': -5,
        'price': 150.0,
        'account_id': '1',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(negative_quantity_order, account_manager)
    assert result is False, "Order with negative quantity should be rejected"

# 6. Order with zero 'quantity'
def test_order_zero_quantity(order_book, account_manager):
    zero_quantity_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 0,
        'price': 150.0,
        'account_id': '2',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(zero_quantity_order, account_manager)
    assert result is False, "Order with zero quantity should be rejected"

# 7. Order with negative 'price'
def test_order_negative_price(order_book, account_manager):
    negative_price_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': -150.0,
        'account_id': '1',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(negative_price_order, account_manager)
    assert result is False, "Order with negative price should be rejected"

# 8. Order with zero 'price' (for limit orders)
def test_order_zero_price_limit(order_book, account_manager):
    zero_price_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 5,
        'price': 0.0,
        'account_id': '2',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(zero_price_order, account_manager)
    assert result is False, "Limit order with zero price should be rejected"

# 9. Order with unsupported 'order_type'
def test_order_unsupported_order_type(order_book, account_manager):
    unsupported_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,
        'account_id': '1',
        'order_type': 'iceberg',  # Unsupported order type
        'timestamp': datetime.now()
    }
    result = order_book.add_order(unsupported_order, account_manager)
    assert result is False, "Order with unsupported order type should be rejected"

# 10. Order with missing 'action' field
def test_order_missing_action(order_book, account_manager):
    missing_action_order = {
        # Missing 'action'
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,
        'account_id': '1',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(missing_action_order, account_manager)
    assert result is False, "Order missing 'action' should be rejected"

# 11. Order with invalid 'action' value
def test_order_invalid_action_value(order_book, account_manager):
    invalid_action_order = {
        'action': 'hold',  # Invalid action
        'ticker': 'AAPL',
        'quantity': 5,
        'price': 150.0,
        'account_id': '2',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(invalid_action_order, account_manager)
    assert result is False, "Order with invalid 'action' value should be rejected"

# 12. Order with future 'timestamp'
def test_order_future_timestamp(order_book, account_manager):
    future_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,
        'account_id': '1',
        'order_type': 'limit',
        'timestamp': datetime.now() + timedelta(days=1)
    }
    result = order_book.add_order(future_order, account_manager)
    assert result is False, "Order with future timestamp should be rejected"

# 13. Order with invalid 'ticker' symbol
def test_order_invalid_ticker(order_book, account_manager):
    invalid_ticker_order = {
        'action': 'sell',
        'ticker': 'INVALID',
        'quantity': 5,
        'price': 150.0,
        'account_id': '2',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(invalid_ticker_order, account_manager)
    assert result is False, "Order with invalid ticker symbol should be rejected"

# 14. Order with extra unexpected fields
def test_order_extra_fields(order_book, account_manager):
    extra_fields_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,
        'account_id': '1',
        'order_type': 'limit',
        'timestamp': datetime.now(),
        'extra_field': 'unexpected_value'  # Extra field
    }
    # Extra fields should not cause rejection as long as required fields are valid
    result = order_book.add_order(extra_fields_order, account_manager)
    assert result is True, "Order with extra fields should be accepted (fields ignored)"

# 15. Order with 'stop_price' in limit order
def test_limit_order_with_stop_price(order_book, account_manager):
    invalid_limit_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 5,
        'price': 150.0,
        'stop_price': 145.0,  # Invalid for limit order
        'account_id': '2',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(invalid_limit_order, account_manager)
    assert result is True, "Having 'stop_price' extra should not directly invalidate a limit order unless logic forbids it"
    # If you want to forbid stop_price in limit orders, you'd have to add explicit checks.
    # Currently, the code ignores fields not required by the order type.

# 16. Stop order with missing 'stop_price'
def test_stop_order_missing_stop_price(order_book, account_manager):
    invalid_stop_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10,
        'account_id': '1',
        'order_type': 'stop_market',
        'timestamp': datetime.now()
        # Missing 'stop_price'
    }
    result = order_book.add_order(invalid_stop_order, account_manager)
    assert result is False, "Stop order missing 'stop_price' should be rejected"

# 17. Market order with 'price' field provided
def test_market_order_with_price(order_book, account_manager):
    invalid_market_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,  # Invalid for market order
        'account_id': '1',
        'order_type': 'market',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(invalid_market_order, account_manager)
    assert result is False, "Market order with 'price' should be rejected"

# 18. Valid market order input
def test_valid_market_order(order_book, account_manager):
    market_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 5,
        'account_id': '2',
        'order_type': 'market',
        'timestamp': datetime.now()
        # No 'price' field
    }
    result = order_book.add_order(market_order, account_manager)
    assert result is True, "Valid market order should be accepted"

# 19. Valid stop order input (stop_market or stop_limit)
def test_valid_stop_order(order_book, account_manager):
    stop_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10,
        'stop_price': 145.0,
        'account_id': '1',
        'order_type': 'stop_market',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(stop_order, account_manager)
    assert result is True, "Valid stop order should be accepted"

# 20. Order with invalid 'account_id'
def test_order_invalid_account_id(order_book, account_manager):
    invalid_account_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 5,
        'price': 150.0,
        'account_id': '999',  # Invalid account ID not in predefined accounts
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    # The system creates new accounts if missing, so this won't fail due to invalid account.
    # If you want to strictly reject unknown accounts, you'd need to add logic for that.
    # Given the current code, this will pass because it creates a new account_id = '999'.
    # Let's assert True since the code will create a new account.
    result = order_book.add_order(invalid_account_order, account_manager)
    assert result is True, "Order with a non-existing account_id creates a new account in current logic."

# 21. Order with insufficient balance (for BUY orders)
# Currently, the code checks balance only at execution time, not at order placement.
# If you wish to test insufficient balance at placement, you'd need to add such logic.
# As is, the order is accepted even if the buyer doesn't have enough balance at order time.
def test_buy_order_insufficient_balance(order_book, account_manager):
    # Large quantity order that would exceed the account's balance if executed
    insufficient_balance_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 100000,  # Very large quantity
        'price': 150.0,
        'account_id': '1',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    # The current code does not reject due to insufficient balance at add time, only at match time.
    # So this will be accepted.
    result = order_book.add_order(insufficient_balance_order, account_manager)
    assert result is True, "Order placement does not check buyer's balance, so it will be accepted."

# 22. Order with insufficient holdings (for SELL orders)
def test_sell_order_insufficient_holdings(order_book, account_manager):
    insufficient_holdings_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 50,  # Exceeds holdings of 20 shares
        'price': 150.0,
        'account_id': '2',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(insufficient_holdings_order, account_manager)
    assert result is False, "SELL order exceeding holdings should be rejected"

# 23. Order with non-existent 'account_id'
def test_order_nonexistent_account(order_book, account_manager):
    # As mentioned, the code creates a new account if it doesn't exist.
    nonexistent_account_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 5,
        'price': 150.0,
        'account_id': '3',  # not initially in account_manager
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    # This will create a new account and accept the order, but since holdings = 0, it should fail the sell.
    result = order_book.add_order(nonexistent_account_order, account_manager)
    assert result is False, "Non-existent account with no holdings cannot sell, should be rejected"

# 24. Order with 'quantity' as float instead of integer
# The code converts quantity to float and checks if > 0, so float is acceptable.
def test_order_quantity_as_float(order_book, account_manager):
    float_quantity_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10.5,  # Quantity as float is allowed in code (converted to float)
        'price': 150.0,
        'account_id': '1',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    # The code allows float quantities since it's converted to float internally.
    result = order_book.add_order(float_quantity_order, account_manager)
    assert result is True, "Float quantity is converted to float and allowed"

# 25. Order with 'price' as string
def test_order_price_as_string(order_book, account_manager):
    string_price_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 5,
        'price': 'one fifty',  # Invalid price
        'account_id': '2',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(string_price_order, account_manager)
    assert result is False, "Order with 'price' as string should be rejected"

# 26. Order with 'quantity' as zero
def test_order_quantity_zero(order_book, account_manager):
    zero_quantity_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 0,
        'price': 150.0,
        'account_id': '1',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(zero_quantity_order, account_manager)
    assert result is False, "Order with 'quantity' as zero should be rejected"

# 27. Order with 'price' as zero in limit order
def test_limit_order_price_zero_again(order_book, account_manager):
    zero_price_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 5,
        'price': 0.0,
        'account_id': '2',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(zero_price_order, account_manager)
    assert result is False, "Limit order with 'price' as zero should be rejected"

# 28. Order with 'ticker' as empty string
def test_order_empty_ticker(order_book, account_manager):
    empty_ticker_order = {
        'action': 'buy',
        'ticker': '',
        'quantity': 10,
        'price': 150.0,
        'account_id': '1',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(empty_ticker_order, account_manager)
    assert result is False, "Order with empty 'ticker' should be rejected"

# 29. Order with 'timestamp' missing
def test_order_missing_timestamp(order_book, account_manager):
    missing_timestamp_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 5,
        'price': 150.0,
        'account_id': '2',
        'order_type': 'limit',
        # Missing 'timestamp'
    }
    result = order_book.add_order(missing_timestamp_order, account_manager)
    assert result is False, "Order missing 'timestamp' should be rejected"

# 30. Order with 'account_id' missing
def test_order_missing_account_id(order_book, account_manager):
    missing_account_id_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,
        # Missing 'account_id'
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(missing_account_id_order, account_manager)
    assert result is False, "Order missing 'account_id' should be rejected"

# 31. Order with negative 'stop_price' in stop order
def test_stop_order_negative_stop_price(order_book, account_manager):
    negative_stop_price_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 5,
        'stop_price': -145.0,  # Invalid stop price
        'account_id': '2',
        'order_type': 'stop_market',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(negative_stop_price_order, account_manager)
    assert result is False, "Stop order with negative 'stop_price' should be rejected"

# 32. Order with invalid 'order_type' value
def test_order_invalid_order_type_value(order_book, account_manager):
    invalid_order_type_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,
        'account_id': '1',
        'order_type': 'fast',  # Invalid order type
        'timestamp': datetime.now()
    }
    result = order_book.add_order(invalid_order_type_order, account_manager)
    assert result is False, "Order with invalid 'order_type' value should be rejected"

# 33. Order with extremely large 'quantity' value
def test_order_extremely_large_quantity(order_book, account_manager):
    large_quantity_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 1000000,  # Extremely large quantity
        'price': 150.0,
        'account_id': '1',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    # The order placement doesn't check balance, so this will be accepted.
    result = order_book.add_order(large_quantity_order, account_manager)
    assert result is True, "Order with extremely large 'quantity' should be accepted at placement"

# 34. Order with extremely large 'price' value
def test_order_extremely_large_price(order_book, account_manager):
    large_price_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 5,
        'price': 1000000.0,  # Extremely large price
        'account_id': '2',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    result = order_book.add_order(large_price_order, account_manager)
    assert result is True, "Order with extremely large 'price' should be accepted at placement"

# 35. Order with 'action' as mixed case (e.g., 'Buy')
def test_order_action_mixed_case(order_book, account_manager):
    mixed_case_action_order = {
        'action': 'Buy',  # Mixed case
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,
        'account_id': '1',
        'order_type': 'limit',
        'timestamp': datetime.now()
    }
    # The code lowercases action, so it should be accepted.
    result = order_book.add_order(mixed_case_action_order, account_manager)
    assert result is True, "Order with 'action' in mixed case should be accepted (case-insensitive)"
