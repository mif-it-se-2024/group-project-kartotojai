# Project Charter

## Business Need / Project Objectives

We need a robust system that can handle real time trading activities efficiently. The platform should address critical aspects like order matching, transaction logging, and seamless handling of various order types (limit, market, stop). Data accuracy, performance, and scalability are essential to ensure smooth operations, even under high volumes. Our goal is to have a platform that mirrors real world financial markets, offering users a reliable and secure environment for trading. The system should not only focus on functionality but also provide opportunities for growth and adaptation as the market evolves.

## Scope

The focus of this project will be on developing a simplified yet robust version of the system. The project will concentrate on creating a console based application for interacting with the system. The goal is to prioritize quality over quantity by ensuring the core functionality order matching, transaction handling, and data management works seamlessly. 

## Deliverables

Console-Based Trading Interface: A command line interface that allows users to place buy/sell orders directly. All user interactions will be handled through the console.
Order Matching System: A core component that matches buy and sell orders based on criteria such as price, quantity, and time. The system will execute trades and update the order book directly in the console.
Transaction Logging: A system that logs all completed trades and stores them either in memory or a local file. The user will be able to access and review past transactions through the console.
Order Book Management: An order book that updates after each transaction or order placement. The current state of the order book (open buy/sell orders) will be displayed in the console.
Trade and Order Report: A function to print a summary of executed trades and the current state of the order book, either to the console or a text file for easy analysis.

## Milestones
1.	2024-10-07	Skeleton creation: Set up the command-line program structure with directories, files, and class definitions (orders, trades, order book).
2.	2024-10-21	Implement order type input: Develop input handling for different order types (limit, market, stop). Validate input and handle incorrect entries with error messages.
3.	2024-11-04	Order matching logic: Implement matching algorithms to process orders. Display matched orders and partial fills directly in the console.
4.	2024-11-18	Integration of match and trade storage: Store matched trades in memory or file. Implement trade report print functionality.
5.	2024-11-30	Console-based order book update: Regularly display the current state of the order book after each transaction or user command.
6.	2024-12-07	Handle edge cases: Implement handling for partial orders, insufficient funds, and all-or-nothing orders. Ensure accurate execution.

## Assumptions and risks

Assumptions:
The project requirements are well defined and wont undergo significant changes after the planning phase. Any major change requests after development starts may cause delays.
It is assumed that the development environment is stable and no major upgrades or changes will be needed mid project.

Risks:
Handling various order types (limit, market, all-or-nothing, partial fills) might introduce complex scenarios that take longer to implement and test, potentially causing delays.
Incorrect trade executions, faulty order matching, or data corruption (especially in user balances) could lead to bugs that require extensive debugging and testing.
If any unexpected issues arise (such as bugs, infrastructure problems, or scope creep), the timeline could be at risk, especially during final testing and optimization.

## Team

| No. | Full name | Group | GitHub username | 
| --- | --------- | ----- | ----------------|
| 1.  | Grantas Bajorūnas | IT 2 (3rd year) | @BilasVartai |
| 2.  | Robertas Kavaliukas | IT 2 (3rd year) | @1LTIS |
| 3.  | Austėja Mikalauskaitė | IT 2 (3rd year) | @aumi8799 |
| 4.  | Karolina Markevičiūtė | IT 2 (3rd year) | @KaroMark |

The whole team will participate in seminars on Tuesdays starting at 14:00.
