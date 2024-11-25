import pytest
import sys
sys.path.insert(0, "C:/Users/auste/Desktop/projektas")
from order_book import OrderBook
from account import AccountManager


@pytest.fixture
def order_book():
    return OrderBook()

@pytest.fixture
def account_manager():
    account_manager = AccountManager()
    account_manager.accounts = {
        "1": {"balance": 10000.0, "positions": {"AAPL": 0}},
        "2": {"balance": 10000.0, "positions": {"AAPL": 10}},
    }
    return account_manager

def test_add_orders_without_saving(order_book, account_manager):
    buy_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10,
        'price': 150.0,
        'account_id': '1',
        'order_type': 'limit',
    }
    result_buy = order_book.add_order(buy_order, account_manager)

    sell_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 5,
        'price': 150.0,
        'account_id': '2',
        'order_type': 'limit',
    }
    result_sell = order_book.add_order(sell_order, account_manager)

    invalid_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': -10, 
        'price': 150.0,
        'account_id': '1',
        'order_type': 'limit',
    }
    result_invalid = order_book.add_order(invalid_order, account_manager)

    assert result_buy is True, "Valid buy order should return True"
    assert result_sell is True, "Valid sell order should return True"
    assert result_invalid is False, "Invalid order should return False"



