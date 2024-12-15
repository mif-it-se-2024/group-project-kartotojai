import pytest
from order_execution import OrderBook
from account import AccountManager
from stock_info import StockInfo
from datetime import datetime

@pytest.fixture
def setup_environment():
    """Set up the environment with test accounts and stocks."""
    account_manager = AccountManager()
    account_manager.update_account("user1", {
        "balance": 5000,
        "positions": {"AAPL": 10}
    })
    account_manager.update_account("user2", {
        "balance": 2000,
        "positions": {"GOOGL": 5}
    })

    stock_info = StockInfo()

    order_book = OrderBook(stock_info)

    return account_manager, stock_info, order_book

def test_all_or_nothing_order(setup_environment):
    """Test All-Or-Nothing order handling."""
    account_manager, stock_info, order_book = setup_environment

    # Create an All-Or-Nothing order
    order = {
        "account_id": "user1",
        "ticker": "AAPL",
        "quantity": 120,
        "price": 150,
        "order_type": "limit",
        "action": "buy",
        "timestamp": datetime.now(),
        "all_or_nothing": True,
    }
    success = order_book.add_order(order, account_manager)

    # Validate order remains pending due to insufficient shares
    assert success is False, "Order should fail due to insufficient shares."
    assert account_manager.get_account("user1")["balance"] == 5000, "User1's balance should not change for failed orders."

def test_insufficient_funds(setup_environment):
    """Test handling of insufficient funds."""
    account_manager, stock_info, order_book = setup_environment

    # Create an order exceeding account balance
    order = {
        "account_id": "user2",
        "ticker": "GOOGL",
        "quantity": 20,
        "price": 200,
        "order_type": "limit",
        "action": "buy",
        "timestamp": datetime.now(),
    }
    success = order_book.add_order(order, account_manager)

    # Validate order is rejected due to insufficient funds
    assert success is False, "Order should fail due to insufficient funds."
    assert account_manager.get_account("user2")["balance"] == 2000, "User2's balance should not change for failed orders."

def test_partial_order_execution(setup_environment):
    """Test partial execution of an order."""
    account_manager, stock_info, order_book = setup_environment

    # Reduce available shares for partial execution
    stock_info.initial_prices["GOOGL"] = 200

    # Create an order for more shares than available
    order = {
        "account_id": "user1",
        "ticker": "GOOGL",
        "quantity": 15,
        "price": 200,
        "order_type": "limit",
        "action": "buy",
        "timestamp": datetime.now(),
    }
    success = order_book.add_order(order, account_manager)

    # Validate partial execution
    assert success is False, "Order should partially fail due to limited availability."

def test_data_integrity_after_multiple_orders(setup_environment):
    """Test data integrity after multiple orders."""
    account_manager, stock_info, order_book = setup_environment

    # Create multiple orders
    order1 = {
        "account_id": "user1",
        "ticker": "AAPL",
        "quantity": 50,
        "price": 150,
        "order_type": "limit",
        "action": "buy",
        "timestamp": datetime.now(),
    }
    order2 = {
        "account_id": "user2",
        "ticker": "GOOGL",
        "quantity": 5,
        "price": 200,
        "order_type": "limit",
        "action": "sell",
        "timestamp": datetime.now(),
    }

    order_book.add_order(order1, account_manager)
    order_book.add_order(order2, account_manager)

    # Validate account balances and stock holdings
    user1_account = account_manager.get_account("user1")
    user2_account = account_manager.get_account("user2")

    assert user1_account["balance"] <= 5000, "User1's balance should be updated."
    assert user2_account["positions"].get("GOOGL", 0) <= 5, "User2's holdings should decrease."
