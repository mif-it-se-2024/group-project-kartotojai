import numpy as np
import pandas as pd

from datetime import datetime, timezone
from typing import List, Dict, Union

from pandas.core.groupby import DataFrameGroupBy
from pandas.core.window import RollingGroupby

class StockFrame:

    def __init__(self, data: List[dict]) -> None:
        """Initializes the StockFrame object.

        Parameters:
        ----
        data (List[dict]): A list of historical price data dictionaries.
        """
        self._data = data
        self._frame: pd.DataFrame = self.create_frame()
        self._symbol_groups: DataFrameGroupBy = None
        self._symbol_rolling_groups: RollingGroupby = None

    @property
    def frame(self) -> pd.DataFrame:
        """Returns the underlying DataFrame."""
        return self._frame
    
    @property
    def symbol_groups(self) -> DataFrameGroupBy:
        """Groups the DataFrame by symbol."""
        self._symbol_groups = self._frame.groupby(
            by='symbol',
            as_index=False,
            sort=True
        )
        return self._symbol_groups
    
    def symbol_rolling_groups(self, size: int) -> RollingGroupby:
        """Creates rolling groups for the symbols.

        Parameters:
        ----
        size (int): The window size for the rolling calculation.

        Returns:
        ----
        RollingGroupby: A rolling groupby object.
        """
        if not self._symbol_groups:
            self.symbol_groups
        self._symbol_rolling_groups = self._symbol_groups.rolling(size)
        return self._symbol_rolling_groups
    
    def create_frame(self) -> pd.DataFrame:
        """Creates a DataFrame from the data provided.

        Returns:
        ----
        pd.DataFrame: A pandas DataFrame with a MultiIndex.
        """
        # Make data frame
        price_df = pd.DataFrame(data=self._data)
        price_df = self._parse_datetime_column(price_df=price_df)
        price_df = self._set_multi_index(price_df=price_df)
        
        # Check for duplicate indices
        duplicate_indices = price_df.index.duplicated()
        if duplicate_indices.any():
            print("Duplicate indices found after creating frame:")
            print(price_df.index[duplicate_indices])
        else:
            print("No duplicate indices after creating frame.")
        
        return price_df


    
    def _parse_datetime_column(self, price_df: pd.DataFrame) -> pd.DataFrame:
        """Parses the 'datetime' column to pandas datetime objects.

        Parameters:
        ----
        price_df (pd.DataFrame): The DataFrame containing the 'datetime' column.

        Returns:
        ----
        pd.DataFrame: The DataFrame with parsed 'datetime' column.
        """
        price_df['datetime'] = pd.to_datetime(price_df['datetime'])
        return price_df
    
    def _set_multi_index(self, price_df: pd.DataFrame) -> pd.DataFrame:
        price_df = price_df.set_index(keys=['symbol', 'datetime'])
        # Drop duplicates
        price_df = price_df[~price_df.index.duplicated(keep='first')]
        return price_df

    
    def add_rows(self, data: List[dict]) -> None:
        """Adds new rows to the StockFrame's DataFrame."""
        # Prepare the new data
        new_data = []

        for quote in data:
            # Parse the timestamp
            if isinstance(quote['datetime'], pd.Timestamp):
                time_stamp = quote['datetime']
            else:
                time_stamp = pd.to_datetime(quote['datetime'])

            # Define the index tuple
            row_id = (quote['symbol'], time_stamp)

            # Skip if the index already exists
            if row_id in self._frame.index:
                continue

            # Append the new row data
            new_data.append({
                'symbol': quote['symbol'],
                'datetime': time_stamp,
                'open': quote['open'],
                'close': quote['close'],
                'high': quote['high'],
                'low': quote['low'],
                'volume': quote['volume']
            })

        if new_data:
            # Create a new DataFrame
            new_rows = pd.DataFrame(new_data)
            new_rows = new_rows.set_index(['symbol', 'datetime'])

            # Append the new rows to the existing DataFrame
            self._frame = pd.concat([self._frame, new_rows])

            # Sort the DataFrame
            self._frame.sort_index(inplace=True)

            # Check for duplicate indices after adding new data
            duplicate_indices = self._frame.index.duplicated()
            if duplicate_indices.any():
                print("Duplicate indices found after adding new rows:")
                print(self._frame.index[duplicate_indices])
            else:
                print("No duplicate indices after adding new rows.")

        # Update the symbol groups
        self.symbol_groups




    def do_indicators_exist(self, column_names: List[str]) -> bool:
        """Checks to see if the indicator columns specified exist.

        Arguments:
        ----
        column_names (List[str]): A list of column names that will be checked.

        Raises:
        ----
        KeyError: If a column is not found in the StockFrame.

        Returns:
        ----
        bool: `True` if all the columns exist.
        """
        if set(column_names).issubset(self._frame.columns):
            return True
        else:
            missing_columns = set(column_names).difference(self._frame.columns)
            raise KeyError(
                f"The following indicator columns are missing from the StockFrame: {missing_columns}"
            )

    def check_signals(
        self,
        indicators: dict,
        indicators_comp_key: List[str],
        indicators_key: List[str]
    ) -> Dict[str, pd.Series]:
        """Returns the signals based on the indicator conditions."""
        # Use the 'indicators' parameter passed to the method
        buys = {}
        sells = {}

        # Check indicators compared to numerical values
        if self.do_indicators_exist(column_names=indicators_key):
            for indicator in indicators_key:
                column = self._symbol_groups.tail(1)[indicator]
                buy_signal = indicators[indicator]['buy']
                sell_signal = indicators[indicator]['sell']
                condition_buy = indicators[indicator]['buy_operator'](column, buy_signal)
                condition_sell = indicators[indicator]['sell_operator'](column, sell_signal)

                if condition_buy.any():
                    buys[indicator] = self._symbol_groups.tail(1)[condition_buy]
                if condition_sell.any():
                    sells[indicator] = self._symbol_groups.tail(1)[condition_sell]

        # Check indicators compared to other indicators
        if self.do_indicators_exist(column_names=indicators_comp_key):
            for indicator in indicators_comp_key:
                ind1, ind2 = indicator.split('_comp_')
                column1 = self._symbol_groups.tail(1)[ind1]
                column2 = self._symbol_groups.tail(1)[ind2]
                buy_operator = indicators[indicator].get('buy_operator')
                sell_operator = indicators[indicator].get('sell_operator')

                if buy_operator:
                    condition_buy = buy_operator(column1, column2)
                    if condition_buy.any():
                        buys[indicator] = self._symbol_groups.tail(1)[condition_buy]
                if sell_operator:
                    condition_sell = sell_operator(column1, column2)
                    if condition_sell.any():
                        sells[indicator] = self._symbol_groups.tail(1)[condition_sell]

        # Combine buys and sells into a dictionary
        signals = {
            'buys': buys,
            'sells': sells
        }

        return signals

    def grab_current_bar(self, symbol: str) -> pd.Series:
        """Grabs the current trading bar for a symbol.

        Parameters:
        ----
        symbol (str): The symbol to grab the latest bar for.

        Returns:
        ----
        pd.Series: A candle bar represented as a pandas Series object.
        """
        # Filter the Stock Frame.
        bars_filtered = self._frame.xs(symbol, level=0, drop_level=False)
        bars = bars_filtered.tail(1)
        return bars

    def grab_n_bars_ago(self, symbol: str, n: int) -> pd.Series:
        """Grabs the trading bar from n bars ago.

        Parameters:
        ----
        symbol (str): The symbol to grab the bar for.
        n (int): The number of bars to look back.

        Returns:
        ----
        pd.Series: A candle bar represented as a pandas Series object.
        """
        # Filter the Stock Frame.
        bars_filtered = self._frame.xs(symbol, level=0, drop_level=False)
        bars = bars_filtered.iloc[-n]
        return bars
