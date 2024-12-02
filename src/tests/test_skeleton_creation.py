import pytest
from stock_info import StockInfo
from order_execution import OrderBook
from account import AccountManager

@pytest.fixture
def stock_info():
    stock_info = StockInfo()
    stock_info.stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA'] 
    return stock_info

@pytest.fixture
def account_manager():
    account_manager = AccountManager()
    account_manager.accounts = {
            "1": {"balance": 10000.0, "positions": {"AAPL": 10}},
            "2": {"balance": 15000.0, "positions": {"MSFT": 5}}
    }  
    return account_manager

def test_stock_info_skeleton(stock_info):
    assert hasattr(stock_info, 'stocks'), "StockInfo class should have an attribute 'stocks'"
    assert hasattr(stock_info, 'is_valid_ticker'), "StockInfo class should have a method 'is_valid_ticker'"
    assert callable(getattr(stock_info, 'is_valid_ticker', None)), "'is_valid_ticker' should be a method"
    assert hasattr(stock_info, 'display_stocks'), "StockInfo class should have a method 'display_stocks'"
    assert callable(getattr(stock_info, 'display_stocks', None)), "'display_stocks' should be a method"
    assert hasattr(stock_info, 'display_stock_info'), "StockInfo class should have a method 'display_stock_info'"
    assert callable(getattr(stock_info, 'display_stock_info', None)), "'display_stock_info' should be a method"

def test_order_book_skeleton():
    order_book = OrderBook()
    assert hasattr(order_book, 'buy_orders'), "OrderBook class should have an attribute 'buy_orders'"
    assert hasattr(order_book, 'sell_orders'), "OrderBook class should have an attribute 'sell_orders'"
    assert hasattr(order_book, 'last_trade_price'), "OrderBook class should have an attribute 'last_trade_price'"

def test_account_manager_skeleton(account_manager):
    assert hasattr(account_manager, 'accounts'), "AccountManager class should have an attribute 'accounts'"
    assert hasattr(account_manager, 'get_account'), "AccountManager class should have a method 'get_account'"
    assert callable(getattr(account_manager, 'get_account', None)), "'get_account' should be a method"
    assert hasattr(account_manager, 'update_account'), "AccountManager class should have a method 'update_account'"
    assert callable(getattr(account_manager, 'update_account', None)), "'update_account' should be a method"
    assert hasattr(account_manager, 'display_account'), "AccountManager class should have a method 'display_account'"
    assert callable(getattr(account_manager, 'display_account', None)), "'display_account' should be a method"
