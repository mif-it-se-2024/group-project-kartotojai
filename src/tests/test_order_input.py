import pytest
import sys
sys.path.insert(0, "C:/Users/auste/Desktop/Projektas2")
from order_book import OrderBook
from account import AccountManager

@pytest.fixture
def order_book():
    return OrderBook()

@pytest.fixture
def account_manager():
    account_manager = AccountManager()
    account_manager.accounts = {
        "1": {"balance": 10000.0, "positions": {"AAPL": 10}},
    }
    return account_manager

def test_valid_limit_order(order_book, account_manager):
    order = {
        'action': 'buy',
        'account_id': '1',
        'ticker': 'AAPL',
        'quantity': 10,
        'order_type': 'limit',
        'price': 150.0
    }
    assert order_book.add_order(order, account_manager) is True

def test_invalid_limit_order_without_price(order_book, account_manager):
    order = {
        'action': 'buy',
        'account_id': '1',
        'ticker': 'AAPL',
        'quantity': 10,
        'order_type': 'limit',
        'price': None
    }
    assert order_book.add_order(order, account_manager) is False

def test_valid_market_order(order_book, account_manager):
    order = {
        'action': 'buy',
        'account_id': '1',
        'ticker': 'AAPL',
        'quantity': 10,
        'order_type': 'market'
    }
    assert order_book.add_order(order, account_manager) is True

def test_invalid_market_order_with_price(order_book, account_manager):
    order = {
        'action': 'buy',
        'account_id': '1',
        'ticker': 'AAPL',
        'quantity': 10,
        'order_type': 'market',
        'price': 150.0
    }
    assert order_book.add_order(order, account_manager) is False

def test_valid_stop_order(order_book, account_manager):
    order = {
        'action': 'sell',
        'account_id': '1',
        'ticker': 'AAPL',
        'quantity': 10,
        'order_type': 'stop',
        'stop_price': 145.0
    }
    assert order_book.add_order(order, account_manager) is True

def test_invalid_stop_order_without_stop_price(order_book, account_manager):
    order = {
        'action': 'sell',
        'account_id': '1',
        'ticker': 'AAPL',
        'quantity': 10,
        'order_type': 'stop',
        'stop_price': None
    }
    assert order_book.add_order(order, account_manager) is False
