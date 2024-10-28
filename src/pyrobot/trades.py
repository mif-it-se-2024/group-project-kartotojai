import uuid
from datetime import datetime
from typing import Dict, Optional, List, Union

class Trade:
    def __init__(self) -> None:
        """Initializes the Trade object."""
        self.order: Dict = {}
        self.order_response: Dict = {}
        self.trades: Dict[str, Dict] = {}
        self.trade_id: Optional[str] = None

    def new_trade(
        self,
        trade_id: str,
        order_type: str,
        enter_or_exit: str,
        long_or_short: str,
        price: float = 0.0,
        stop_limit_price: float = 0.0
    ) -> Dict:
        """Creates a new trade with the specified parameters.

        Parameters:
        ----
        trade_id (str): A unique identifier for the trade.
        order_type (str): The type of the order (e.g., 'mkt', 'lmt', 'stop', 'stop_lmt').
        enter_or_exit (str): Whether to enter or exit a position ('enter' or 'exit').
        long_or_short (str): Whether the trade is 'long' or 'short'.
        price (float, optional): The price for limit or stop orders.
        stop_limit_price (float, optional): The stop price for stop-limit orders.

        Returns:
        ----
        Dict: The initial order dictionary.
        """
        self.trade_id = trade_id

        # Define order instructions
        self.order_instructions = {
            'enter': {
                'long': 'BUY',
                'short': 'SELL_SHORT'
            },
            'exit': {
                'long': 'SELL',
                'short': 'BUY_TO_COVER'
            }
        }

        # Map order types to their respective identifiers
        self.order_types = {
            'mkt': 'MARKET',
            'lmt': 'LIMIT',
            'stop': 'STOP',
            'stop_lmt': 'STOP_LIMIT',
            'trailing_stop': 'TRAILING_STOP'
        }

        # Build the initial order dictionary
        self.order = {
            "order_id": self._generate_order_id(),
            "order_type": self.order_types[order_type],
            "enter_or_exit": enter_or_exit,
            "long_or_short": long_or_short,
            "price": price,
            "stop_limit_price": stop_limit_price,
            "instrument": {
                "symbol": None,
                "quantity": 0,
                "asset_type": None
            },
            "timestamp": datetime.now().isoformat()
        }

        return self.order

    def instrument(
        self,
        symbol: str,
        quantity: int,
        asset_type: str,
        order_leg_id: int = 0
    ) -> None:
        """Sets the instrument for the trade.

        Parameters:
        ----
        symbol (str): The ticker symbol of the asset.
        quantity (int): The number of shares to trade.
        asset_type (str): The type of the asset (e.g., 'EQUITY').
        order_leg_id (int, optional): The order leg identifier.
        """
        self.order['instrument']['symbol'] = symbol
        self.order['instrument']['quantity'] = quantity
        self.order['instrument']['asset_type'] = asset_type

    def add_stop_loss(
        self,
        stop_price: float
    ) -> None:
        """Adds a stop-loss order to the trade.

        Parameters:
        ----
        stop_price (float): The price at which the stop-loss order will be triggered.
        """
        self.order['stop_loss'] = {
            'price': stop_price
        }

    def add_take_profit(
        self,
        profit_price: float
    ) -> None:
        """Adds a take-profit order to the trade.

        Parameters:
        ----
        profit_price (float): The price at which the take-profit order will be triggered.
        """
        self.order['take_profit'] = {
            'price': profit_price
        }

    def _generate_order_id(self) -> str:
        """Generates a unique order ID.

        Returns:
        ----
        str: A unique order identifier.
        """
        return str(uuid.uuid4())

    @property
    def order_response(self) -> Dict:
        """Gets the order response.

        Returns:
        ----
        Dict: The order response dictionary.
        """
        return self._order_response

    @order_response.setter
    def order_response(self, order_response_dict: Dict) -> None:
        """Sets the order response.

        Parameters:
        ----
        order_response_dict (Dict): The response dictionary from order execution.
        """
        self._order_response = order_response_dict

    def modify_order(
        self,
        price: Optional[float] = None,
        stop_limit_price: Optional[float] = None,
        quantity: Optional[int] = None
    ) -> None:
        """Modifies the existing order with new parameters.

        Parameters:
        ----
        price (float, optional): The new price for limit or stop orders.
        stop_limit_price (float, optional): The new stop price for stop-limit orders.
        quantity (int, optional): The new quantity for the order.
        """
        if price is not None:
            self.order['price'] = price
        if stop_limit_price is not None:
            self.order['stop_limit_price'] = stop_limit_price
        if quantity is not None:
            self.order['instrument']['quantity'] = quantity

    def cancel_order(self) -> None:
        """Cancels the order."""
        self.order['status'] = 'CANCELLED'
