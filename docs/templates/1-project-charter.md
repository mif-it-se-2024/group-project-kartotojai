# Project Charter

## Business Need / Project Objectives

Financial exchanges replicate actual markets. It involves real world challenges like data accuracy, performance etc. It provides a strong practical foundation. The project will likely involve algorithms for matching buyers and sellers, pricing models, and possibly transaction logging. This helps with problem solving skills.

## Scope

User registration, order placement and matching, order placement and matching, real time data handling, transaction handling, database management, 

## Deliverables

Order Matching System - a system where users can register, log in, and interact with a market for buying and selling financial assets. A core component responsible for efficiently matching buy and sell orders based on criteria like price, quantity and time.

## Milestones

1. Project Setup and Requirements Gathering
2. User Registration and Authentication
3. Implement Order Placement System
4. Build the Matching Engine
5. Trade Execution and Recording
6. Real Time Order Book Updates
7. Error Handling and Edge Cases
8. Final Testing and Optimization
   
| No. | Target date  | Description |
| --- | ----------- | ----------- |
| 1.  | 2024-10-07 | Define the core features (order types, matching system). Set up the project environment and database schema. |
| 2.  | 2024-10-21 | Build order submission forms for orders. Validate orders before they are submitted to the system. |
| 3.  | 2024-11-04 | Develop the core logic to match buy and sell orders. Implement partial matching and ensure unmatched orders are saved. |
| 4.  | 2024-11-18 | Create the system to execute trades and update user balances. Store trade history and adjust or remove orders from the order book. |
| 5.  | 2024-11-30 | Implement real-time order book updates. Ensure live data is updated immediately after new trades and orders. |
| 6.  |  2024-12-07 | Handle edge cases (e.g., partial orders, insufficient funds). Make sure all-or-nothing orders work correctly. |
| 7.  |  2024-12-14 | Test the system thoroughly with real and edge-case scenarios. Optimize performance and finalize all documentation. |

## Assumptions and risks

Assumptions:
The project requirements are well defined and wont undergo significant changes after the planning phase. Any major change requests after development starts may cause delays.
It is assumed that the development environment (tech stack, libraries, database systems) is stable and no major upgrades or changes will be needed mid-project.

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
