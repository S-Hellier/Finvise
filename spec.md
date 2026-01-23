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

* Account Integration
    - Plaid will handle integration with existing accounts

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
             - Id
             - Name (Account name given by user)
             - Last 4 Digits of Account Number
             - Type (AccountType item)
             - Subtype (AccountSubtype item)
             - Current Balance
             - Available Balance (Funds available for immediate withdraw)
             - Credit Limit (If applicable)
             - Currency (Default USD)
             - Institution ID
        * AccountType (ENUM)
            - Depository, Credit, Investment, Loan, Other
        * AccountSubType (ENUM)
            - Checking, Saving, Credit Card, IRA, 401K, Mortgage, etc.
        * Dependent
            - Id
            - Name
            - Relationship (UserRelationshipType)
            - Birthdate (Derive Age)
            - Major Expenses (List of 'Tags' to be used by the model, including things like Daycare, College Fund, Tuition, Health Insurance, etc)
        * UserRelationshipType (ENUM)
            - Child, Partner, Spouse, Parent, Other
        * Asset
            - Id
            - Account Id (Account holding the asset)
            - Symbol (Ticker symbol if a stock)
            - Name (Colloquial name of the asset)
            - Class (AssetClass Object)
            - Quantity (Number of units of the asset, should be float)
            - Cost (Amount paid to acquire the asset)
            - Current Price (Last known market price)
            - Last Updated (Date attribute reflecting when the market price was last updated)
            - Derived Market Value (Price * Quantity)
            - Derived Net (Market Value - Cost)
            - Derived Percent Return
        * AssetClass (ENUM)
            - Equity, Fixed, Crypto, Real Estate, Commodity (Gold, Silver, etc), Collectible (Art, Watches, Antiques, etc)
    2. Create Pandas SQLite Data Pipeline
        * Build a Data ingestor that uses Pandas to convert CSV bank Statements or JSON data from Plaid into structured Database information via the existing schema.
        * When a user uploads a CSV or the app recieves JSON data from Plaid, this Pandas functionality should complete the pipeline that transforms this financial information into readily accessible and easily digestible user information for the model to work with
        * This ingestor should handle common CSV conventions for organizing data from financial information, including transforming dates to the proper format, Interpreting column names to their proper semantic meaning as defined by the SQLite databse, and extrapolating meaning from the column items if needed.
        * LLM assistance should be implemented for this data processing component. A Small model should do the job of interpreting the relationships between the ingested column names and their representation in the database, as well as extrapolating as much information as possible from column items for use in the database
    3. SQL Tooling
        * Create Python functionality that allows an LLM to easily inspect the database schema and execute read-only queries
            - This may include functionality like listing tables, columns, and their descriptions

2. Phase 2: Knowledge RAG (Unstructured Data)
    Give the LLM the foundational financial knowledge, both from generally available sources and the user's personal financial preferences, so that it can effectively answer questions in a personally and wisely fine-tuned manner
    1. Vector Ingestion: 
        * Set up ChromaDB database for embeddings
        * Implement a pipeline to chunk and embed financial PDFs and other common document types
            - Chunking should be done in a semantically meaningful way in accordance to the most up-to-date industry best-practices
            - User-submitted documents should be supported. For example, if there is a document on financial philosophy that the user finds particularly compelling, they can input this document and have it be embedded in the knowledge base. 
    2. Retrieval Logic:
        * Implement a Hybrid Search retriever
            - Semantic meaning is certainly important when dealing with financial concepts, but keywords are extremely important as well. If a user is looking for information on a 401k or Roth IRA, documents that explicitly discuss these terms should be prioritized
    3. Context-Augmented Q&A functionality (Basic RAG)
        * Create basic LangChain loop that answers straight forward knowledge questions based on uploaded knowledge base.
            - Examples might include "What is a 401k?", "Are stocks generally riskier that bonds?", "In what situations would it be advisable to go into debt?", or "How does an HSA account work?"
            - More targeted examples based on the specific uploaded documents might be "What would a combined financial philosophy between Warren Buffett and Dave Ramsey have to say about investing in individual stocks over ETFs?" or "Does my grandfather's financial philosophy (found in an uploaded document) align with the teachings of 'Rich Dad Poor Dad'?"

3. Phase 3: LangGraph Orchestration
    This phase provides the transition from simple chains to an actual agentic state machine
    1. State Definition:
        * Define `GraphState` using TypedDict to track message history, retrieved data, and intermediate SQL results.
    2. Router Node
        * Build logic that decides query needs
            - Do I need to query the SQL DB?
            - Do I need to query the vector DB?
            - Do I need to perform a calculation?
    3. Integrate Tools
        * Bind SQL tooling, calculator, and RAG retriever as tools that the Agent can call. 
        * The calculator should be a Python module that handles calculations separately from the LLM.
            - Should include functions for calculating compound interest, estimating taxes, a SQL aggregator for calculations within the SQLite Database, etc.