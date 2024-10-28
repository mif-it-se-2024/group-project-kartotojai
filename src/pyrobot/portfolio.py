from typing import List, Tuple, Dict, Union, Optional


class Portfolio:

    def __init__(self, account_number: Optional[str] = None):
        self.positions: Dict[str, Dict[str, Union[str, float, int, bool]]] = {}
        self.positions_count: int = 0
        self.market_value: float = 0.0
        self.profit_loss: float = 0.0
        self.risk_tolerance: float = 0.0
        self.account_number: Optional[str] = account_number


    #add error handling
    def add_position(
        self,
        symbol: str,
        asset_type: str,
        purchase_date: Optional[str] = None,
        quantity: int = 0,
        purchase_price: float = 0.0,
        owned: bool = False  # The correct parameter is 'owned'
    ) -> Dict[str, Dict]:
        """Adds a single position to the portfolio."""
        self.positions[symbol] = {
            'symbol': symbol,
            'quantity': quantity,
            'purchase_price': purchase_price,
            'purchase_date': purchase_date,
            'asset_type': asset_type,
            'owned': owned
        }
        return self.positions


    def add_positions(self, positions: List[dict]) -> Dict[str, Dict]:
        """Adds multiple positions to the portfolio."""

        if isinstance(positions, list):
            for position in positions:
                self.add_position(
                    symbol=position['symbol'],
                    asset_type=position['asset_type'],
                    purchase_date=position.get('purchase_date', None),
                    purchase_price=position.get('purchase_price', 0.0),
                    quantity=position.get('quantity', 0),
                    ownership_status=position.get('ownership_status', False)
                )
            return self.positions
        else:
            raise TypeError("Positions must be a list of dictionaries")

    def remove_position(self, symbol: str) -> Tuple[bool, str]:
        """Removes a position from the portfolio."""

        if symbol in self.positions:
            del self.positions[symbol]
            return True, f"{symbol} was successfully removed"
        else:
            return False, f"{symbol} did not exist in the portfolio."

    def set_ownership_status(self, symbol: str, ownership: bool) -> None:
        """Sets the ownership status of a position.

        Parameters:
        ----
        symbol (str): The ticker symbol of the asset.
        ownership (bool): True if owned, False if not.
        """
        if symbol in self.positions:
            self.positions[symbol]['owned'] = ownership
        else:
            # If the symbol is not in positions, you might want to add it or handle it accordingly
            self.positions[symbol] = {
                'symbol': symbol,
                'quantity': 0,
                'purchase_price': 0.0,
                'purchase_date': None,
                'asset_type': 'equity',
                'owned': ownership
            }

    def get_ownership_status(self, symbol: str) -> bool:
        """Gets the ownership status of a position.

        Parameters:
        ----
        symbol (str): The ticker symbol of the asset.

        Returns:
        ----
        bool: True if the asset is owned, False otherwise.

        Raises:
        ----
        KeyError: If the symbol is not found in the portfolio.
        """
        if symbol in self.positions:
            return self.positions[symbol].get('ownership_status', False)
        else:
            raise KeyError(f"Symbol {symbol} not found in portfolio.")

    def total_allocation(self) -> float:
        """Calculates the total allocation of the portfolio."""

        total_allocation = sum(
            position['quantity'] * position['purchase_price']
            for position in self.positions.values()
        )
        self.market_value = total_allocation
        return total_allocation

    def risk_exposure(self) -> float:
        """Calculates the risk exposure of the portfolio."""

        # Placeholder implementation; customize based on risk calculation
        self.risk_tolerance = self.market_value * 0.1  # Example: 10% of market value
        return self.risk_tolerance

    def in_portfolio(self, symbol: str) -> bool:
        """Checks if a symbol is in the portfolio."""

        return symbol in self.positions

    def is_profitable(self, symbol: str, current_price: float) -> bool:
        """Determines if a position is profitable."""

        if symbol in self.positions:
            purchase_price = self.positions[symbol]['purchase_price']
            return current_price >= purchase_price
        else:
            raise KeyError(f"Symbol {symbol} not found in portfolio.")
