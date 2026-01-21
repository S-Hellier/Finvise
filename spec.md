## Overview:
Finvise is an individualized AI financial advisor. 
Users input their financial demographic information, financial philosphies, and financial accounts as part of their Finvise account information.
Finvise then uses the user's personal information, as well as the most up-to-date financial information regarding markets, inflation, future trends, etc. to answer user-generated questions regarding financial information or advice. It can also offer unsolicited advice in the form of notifications based on currently available information.
Finvise will use an LLM in combination with Retrieval Augmented Generation techniques to make decisions, answer questions, and just generally understand the interplay between broader financial principles and trends with the user's unique financial details. 

### Some Use Case Examples:
* What are some holes in my current financial plan if I want to retire at 50?
* I'm expecting a child within the next year. How can I plan ahead for this?
* Can I afford a new Tesla right now?
* Did I overspend on clothing last year?
* What's a good credit card to get to expand my portfolio?

## Technical Specifications
* LLMs
    - Ollama: on-device LLM ensures privacy of the highly sensitive information that will pass through the model.

* Task Orchestration:
    - LangGraph will be used for task orchestration. The complex nature of answering certain queries, including parsing personal information for a variety of data in various formats, means that LangGraph would be ideal over simple LangChain.

* Vector Databases:
    - ChromaDB: For storing embeddings to be used in semantic search

* Structured Data:
    - SQLite: For specific, time-bound personal financial information
    - Pandas: For complex data calculations on stored data

* Validation:
    - Pydantic: Ensure formatting consistency for LLMs

## Roadmap:

1. Phase 1: Structured Storage
    1. Generate Pydantic schema for:
        * User
            - Id
            - Email
            - Password
            - Financial Philosophy
                - The financial philosophy should be a user-submitted document detailing the way the user thinks about finances and the user's financial goals. Examples for sections that might be included in the document could be "I'm young, single, and without dependents; at this point in my life I'm willing to take reasonable risks for large financial gain" or "Avoiding debt is the most important financial principle for me."
            - Accounts (dictionary that maps to Account data types)
            - Birthdate -> Derived Age (optional)
            - Dependents (List of dependent types)
            - Assets (List of Asset types)
            - Net Worth (Derived)
        * Transaction
            - Transaction Id
            - Account Id
            - Date
            - Name (Name of the transaction given by the financial institution)
            - Amount
            - Currency (ISO currency code, default to USD)
            - Direction (Inflow or Outflow)
            - Status (Pending, Posted)
            - Category (Dining, Groceries, Rent, Clothing, etc)
            - Transfer (Boolean determining if the transaction is a transfer within the user's own accounts)
        * Account
        * Dependent
        * Asset