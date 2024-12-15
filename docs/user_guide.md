# User Guide: Setting Up the Order Matching System

Welcome to the **Order Matching System**! We hope this guide will provide all the instructions to set up, run, and use the system effectively.

---

## Precondition

Before starting, ensure that your system meets the following requirements:

- **Python 3.8+**: Download and install from [python.org](https://www.python.org/downloads/).
- **Git**: Download and install from [git-scm.com](https://git-scm.com/).

---

## Setup Instructions

### 1. Clone the Repository


```
git clone https://github.com/mif-it-se-2024/group-project-kartotojai
cd group-project-kartotojai
```

### 2. Install Python Dependencies


```
pip install -r requirements.txt
```

### 3. Navigate to the Source Directory

```
cd src
```

---

## How to Run the System

### 1. Start the Program: 
Run the following command in the terminal: 

```
python main.py
```
### 2. Interactive commands:

Once the system is running, you will see a welcome message:
```
Welcome to the Stock Trading Simulator!
Type 'help' to see available commands.
```

### 3. Type **help** to view the list of commands available.
```
help
```

---

## Command Overview

The system supports the following commands:

### General Commands

**`help`**: Displays a list of all available commands.

**`exit`**: Exits the program.

### Account Management Commands

**`account info <account_id>`**: Displays details about the specified account, such as balances and positions.

**`reset`**: Resets all accounts and order books to their default state.

### Order Placement Commands

**`buy <account_id> <ticker> <quantity> [order_type] [price]`**: Places a buy order for the specified account.

Example:
```
buy 1 AAPL 10 limit 150
```
**`sell <account_id> <ticker> <quantity> [order_type] [price]`**: Places a sell order for the specified account.

Example:
```
sell 2 TSLA 5 market
```
**`stop buy <account_id> <ticker> <quantity> market <stop_price>`**: Places a stop-market buy order.

**`stop sell <account_id> <ticker> <quantity> market <stop_price>`**: Places a stop-market sell order.

**`stop buy <account_id> <ticker> <quantity> limit <stop_price> <limit_price>`**: Places a stop-limit buy order.

**`stop sell <account_id> <ticker> <quantity> limit <stop_price> <limit_price>`**: Places a stop-limit sell order.

**`cancel <account_id> <order_id>`**: Cancels a specified order.

**`cancel stop <account_id> <order_id>`**: Cancels a specified stop order.

### Information Retrieval Commands

**`stock info [<ticker>]`**: Displays information about a specific stock or all stocks if no ticker is provided.

Example:
```
stock info AAPL
```

**`order book`**: Displays the current state of the order book.

**`order stop book`**: Displays all active stop orders.

### Trade History Commands

**`executed trades display`**: Displays a list of all executed trades.

**`executed trades export <filename>`**: Exports the executed trades to a specified file.

Example:
```
executed trades export trades.csv
```

**`executed trades delete <trade_id>`**: Deletes a specific executed trade by its ID.

## Example Workflow

### Placing a Limit Order

#### Start the program:
```
python main.py
```
#### View your account details:
```
account info 1
```
#### Place a limit buy order:
```
buy 1 AAPL 10 limit 150
```
#### View the order book:
```
order book
```
#### Exit the system:
```
exit
```
---
## Explanation of Key Concepts

### Tickers

Tickers are symbols representing publicly traded companies or financial instruments. For example:

**AAPL:** Apple Inc.

**TSLA:** Tesla Inc.

**GOOG:** Alphabet Inc. (Google)

Tickers are used to specify the stock or instrument you want to trade.

### Order Types

The system supports several order types:

**Market Order:** An order to buy or sell immediately at the best available price.

**Limit Order:** An order to buy or sell at a specific price or better.

**Stop Order:** An order that becomes active only when a specified trigger price is reached.

**Stop-Market Order:** Executes as a market order once triggered.

**Stop-Limit Order:** Executes as a limit order once triggered.

---
Thank you for using the Order Matching System!



