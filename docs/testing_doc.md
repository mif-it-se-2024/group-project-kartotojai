## Testing Documentation for the Order Matching System

This document provides an overview of the testing process implemented in the Order Matching System project.

---

### Testing Tools and Frameworks
The following tools and libraries were used for testing:

**pytest:** A Python testing framework used for writing and executing automated tests.

**flake8:** A code linting tool to ensure adherence to coding standards.

---

### Running the Tests

Follow these steps to execute the tests:

1 . Install the Dependencies:

You can install dependencies in one of two ways:

- Using the **`requirements.txt`** file (recommended):

```
pip install -r requirements.txt
```
- Installing **`pytest`** individually:

```
pip install pytest
```

2. Navigate to the Project Directory:

```
cd src
```
3. Run All Tests:

Execute the following command to run all test files:

```
pytest tests
```

4. Run Specific Test Files:

To run a specific test file, use:

```
pytest tests/test_order_input.py
```
---

### Test Results

#### Coverage

The tests cover the following key components:

- Order input validation

- Order matching logic

- Integration of match and trade storage

- Edge case scenarios

- Console-based order book update

#### Results
```
============================= test session starts ==============================
platform linux -- Python 3.10.15, pytest-8.3.3, pluggy-1.5.0
rootdir: /home/runner/work/group-project-kartotojai/group-project-kartotojai
collected 68 items

src/tests/test_console_based_update.py .                                 [  1%]
src/tests/test_edge_cases.py ....                                        [  7%]
src/tests/test_match_trade_storage.py ....                               [ 13%]
src/tests/test_order_input.py ....................................       [ 66%]
src/tests/test_order_matching.py ....................                    [ 95%]
src/tests/test_skeleton_creation.py ...                                  [100%]

============================== 68 passed in 0.40s ==============================
```
---
### Description of Tests

**`test_skeleton_creation.py`**

**What it does:** Tests the basic structure of key components.

Checks if core classes like StockInfo, OrderBook, and AccountManager are set up correctly.

Verifies attributes, methods, and initial values.

**`test_order_input.py`**

**What it does:** Checks if user inputs for orders are valid.

Tests valid and invalid inputs for BUY and SELL orders.

Handles missing fields, wrong data types, and invalid quantities.

Ensures proper error handling for invalid or missing account IDs.

**`test_order_matching.py`**

**What it does:** Tests the main matching logic.

Verifies correct matching for BUY and SELL orders.

Tests price and time priority for order execution.

Ensures correct handling of partial matches and remainders.

**`test_match_trade_storage.py`**

**What it does:** Tests how orders are matched and stored.

Verifies full and partial matches between buy and sell orders.

Ensures unmatched orders stay in the order book.

Confirms trades are recorded correctly in trade history.

**`test_console_based_update.py`**

**What it does:** Tests updates shown in the console.

Checks if the order book is displayed correctly after changes.

Verifies outputs for successful orders and cancellations.

Ensures error messages are shown for invalid operations.

**`test_edge_cases.py`**

**What it does:** Tests how the system handles unusual situations.

Checks orders with insufficient balances or stocks.

Tests large inputs, invalid tickers, and edge scenarios.

Ensures the system rejects invalid and extreme inputs correctly.

---

