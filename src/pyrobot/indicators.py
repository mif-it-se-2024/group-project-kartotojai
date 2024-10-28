import pandas as pd
from typing import Dict, Optional, Any

from pyrobot.stock_frame import StockFrame

class Indicators:

    def init(self, price_data_frame: StockFrame) -> None:
        self._stock_frame: StockFrame = price_data_frame
        self._price_groups = self._stock_frame.symbol_groups
        self._indicator_signals: Dict[str, Dict[str, Any]] = {}
        self._frame: pd.DataFrame = self._stock_frame.frame

    def set_indicator_signals(
        self,
        indicator: str,
        buy: Optional[float] = None,
        sell: Optional[float] = None,
        condition_buy: Optional[str] = '>',
        condition_sell: Optional[str] = '<'
    ) -> None:
        """Sets the buy and sell signals for a given indicator."""
        if indicator not in self._indicator_signals:
            self._indicator_signals[indicator] = {}

        self._indicator_signals[indicator]['buy'] = buy
        self._indicator_signals[indicator]['sell'] = sell
        self._indicator_signals[indicator]['buy_operator'] = condition_buy
        self._indicator_signals[indicator]['sell_operator'] = condition_sell

    def get_indicator_signals(self, indicator: Optional[str] = None) -> Dict:
        """Retrieves the indicator signals."""
        return self._indicator_signals.get(indicator, self._indicator_signals)

    def check_signals(self) -> Optional[pd.DataFrame]:
        """Checks for buy and sell signals based on the indicators."""
        indicators_key = []
        indicators_comp_key = []

        for indicator in self._indicator_signals.keys():
            if 'comp' in indicator:
                indicators_comp_key.append(indicator)
            else:
                indicators_key.append(indicator)

        signals = self._stock_frame.check_signals(
            indicators=self._indicator_signals,
            indicators_comp_key=indicators_comp_key,
            indicators_key=indicators_key
        )

        return signals
