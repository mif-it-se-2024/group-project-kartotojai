import pytest
import sys
sys.path.insert(0, "C:/Users/auste/Desktop/projektas")
from order_book import OrderBook
from datetime import datetime

def test_add_valid_stop_order(order_book, account_manager):
    stop_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 10,
        'order_type': 'stop',
        'stop_price': 145.0,
        'account_id': '1',
        'timestamp': datetime.now()
    }
    assert order_book.add_order(stop_order, account_manager) is True, "Valid stop order should be accepted"

def test_reject_stop_order_without_stop_price(order_book, account_manager):
    stop_order = {
        'action': 'sell',
        'ticker': 'AAPL',
        'quantity': 10,
        'order_type': 'stop',
        'stop_price': None,  
        'account_id': '1',
        'timestamp': datetime.now()
    }
    assert order_book.add_order(stop_order, account_manager) is False, "Stop order without stop price should be rejected"

def test_reject_stop_order_with_invalid_stop_price(order_book, account_manager):
    stop_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10,
        'order_type': 'stop',
        'stop_price': -10.0,  
        'account_id': '2',
        'timestamp': datetime.now()
    }
    assert order_book.add_order(stop_order, account_manager) is False, "Stop order with negative stop price should be rejected"

def test_activate_stop_order(order_book, account_manager):
    stop_order = {
        'action': 'buy',
        'ticker': 'AAPL',
        'quantity': 10,
        'order_type': 'stop',
        'stop_price': 145.0,
        'account_id': '1',
        'timestamp': datetime.now()
    }
    assert order_book.add_order(stop_order, account_manager) is True, "Valid stop order should be accepted"

    order_book.update_market_price('AAPL', 145.0)

    assert 'AAPL' in order_book.buy_orders, "Stop order should be moved to buy_orders after being triggered"
    assert len(order_book.buy_orders['AAPL']) > 0, "Buy orders for AAPL should not be empty"
