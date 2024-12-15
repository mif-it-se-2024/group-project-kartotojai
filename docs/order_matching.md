# Order Matching System Documentation

Welcome to the **Order Matching System**! We hope this guide will provide a comprehensive explanation of our order matching system that is a key part of this project. It allows for fast and fair trading by matching buy and sell orders in real-time. This document explains how the system works, including its structure, how it operates, and how it handles different situations.


---
## Matching System Design
### Key Concepts

---

### 1.	Order Types:



-	**Market Orders**: These orders are carried out right away at the best price available.
-	**Limit Orders**: These orders are only carried out at a set price or better.
-	**Stop Orders**: These orders are activated when the price reaches a certain level, turning into market or limit orders.



### 2. Order Books:

-	Orders are stored in lists called deques for both buying and selling. This makes accessing and managing them fast.
-	Stop orders are kept in separate lists until they are activated.


### 3. Matching Priorities:

-	**Price Priority**: Higher-priced buy orders are matched first. Lower-priced sell orders take priority.
-	**FIFO Rule**: If two orders have the same price, the oldest one is handled first.

### 4. Dynamic Updates:

-	**Last Trade Price**: The system keeps track of the last price at which a trade was made. This is important for activating stop orders and keeping the market data current.

---

### Components

---

### 1.	Order Books: 

-	**Buy Orders:** 
    -	A list of buy orders sorted by price and time.
-	**Sell Orders:** 
    - A list of sell orders sorted by price and time.
-	**Stop Orders:**
    
    -	Stop Buy Orders: Activated when the market price goes above or equals the stop price.
    - Stop Sell Orders: Activated when the market price goes below or equals the stop price.


### 2.	Executed Trades:

- Trades that have been completed are saved in a file (executed_trades.json). Each trade includes details like trade ID, stock ticker, price, quantity, and the accounts involved.

### 3. Validation
- The system checks each order to ensure quantities, prices, and other details are correct.
- It also checks if the buyer has enough money or the seller has enough stock.

---

### Matching Workflow

---

### 1.	Order Entry: 

-	New orders are checked to make sure they follow the rules (e.g., positive quantities and valid prices).
-	Valid orders are added to the buy, sell, or stop order lists.


### 2.	Order Matching:

-	A buy order is matched with a sell order if the buy price is equal to or greater than the sell price.
-	The trade price is set based on the type of orders:

    -	For a market buy and limit sell: The trade happens at the sell price.
    -	For a limit buy and market sell: The trade happens at the buy price.
    -	For two limit orders: The trade happens at the sell price, if the buy price meets or beats it.


### 3. Matching Logic Details:

-	Orders are iteratively checked for matches.
-	A match happens if:

    - The buy price (limit) is greater than or equal to the sell price.
    - For market orders, the match happens with the best price from the opposing order book.
- After a match is found:

    - The execution price is determined by:

        - The price of the limit order in a market-limit combination.
        - The sell price for two limit orders.
        - The last trade price for two market orders.

  - The trade quantity is set to the smaller of the two order quantities.

### 4.	Execution:

- The buyer's and seller's accounts are updated:

  - The buyer's account balance is reduced by the trade amount.
  - The buyer's stock holdings are increased.
  - The seller's stock holdings are decreased, and their balance is increased by the trade amount.

- If an order is fully matched, it is removed from the order book.
- If only partially matched, the remaining quantity stays in the book.


### 5.	Stop Orders:

- When the market price meets the stop price, stop orders are activated and converted into limit or market orders.
- The newly activated orders enter the matching process.


### 6.	Edge Case Handling in Matching:

- **No Match Available:** If no match is found, the order remains in the book.
- **Multiple Matches:** A single order can match with multiple opposing orders if quantities align.
- **FIFO Conflicts:** Among orders with the same price, the system always processes the oldest order first.

---

### Advanced Features

---

### 1.	Dynamic Price Updates:

- After each trade, the last trade price is updated, ensuring stop orders are triggered correctly.

### 2.	High-Speed Matching:

- The system uses fast data structures, so orders can be processed quickly, even when there are many.

### 3.	Trade Records:

- All trades are logged, creating a clear history for auditing and review.

### 4.	Handling Special Cases:

- **Invalid Orders:** Orders with negative quantities or prices are not allowed.
- **Insufficient Funds or Stocks:** Orders are checked to ensure the buyer has enough money or the seller has enough stocks.
- **Price Gaps:** Orders stay in the book if no match is available until market conditions change.

---

### Example Scenarios

---

### 1.	Exact Match:

- A buy limit order for 10 shares at $150 matches a sell limit order for 10 shares at $150.
- The trade happens at $150, and both orders are removed.

### 2.	Partial Match:

- A buy limit order for 15 shares at $150 matches a sell limit order for 10 shares at $150.
- 10 shares are traded at $150. The buy order now has 5 shares left.

### 3.	No Match:

- A buy limit order for 10 shares at $140 is added, but the lowest sell price is $150.
- The buy order waits in the order book for a matching sell order.

### 4.	Stop Order Trigger:

- A stop sell order for 10 shares with a stop price of $145 is triggered when the market price hits $145.
- It turns into a market sell order and is matched with the best available buy order.


---

## Code Insights


### Order Matching Algorithm

---

- **The match_orders function is the main part of the matching process:**

    #####  1. Sorting Orders:
    - Buy orders are sorted so higher prices come first. If prices are the same, older orders come first.
    - Sell orders are sorted so lower prices come first. If prices are the same, older orders come first.
    
    
    #####  2.	Matching Loop:
    - The system compares buy and sell orders one by one to find matches.
    - It checks if the buy price meets or exceeds the sell price. If yes, a trade happens.
    - The trade price is based on the type of orders (e.g., market or limit).
    
    #####  3.	Execution:
    - The trade quantity is the smaller of the two order quantities.
    - Buyer’s money and seller’s stocks are updated to reflect the trade.
    - If an order is fully traded, it is removed from the book. If only part is traded, the remaining part stays.
    
    
    #####  4.	Handling Special Cases:
    - If there are no matches, the order remains in the book.
    - Partially matched orders are kept with updated quantities.
    
    
---

### Stop Order Handling

---   
    
    
- **The check_stop_orders function ensures stop orders are triggered at the right time:**
    - Stop Buy Orders:
        - Turn into regular buy orders when the market price is equal to or higher than the stop price.
        
    - Stop Sell Orders:
        - Turn into regular sell orders when the market price is equal to or lower than the stop price.
    
    - Once triggered, these orders are added to the order books and matched like other orders.

