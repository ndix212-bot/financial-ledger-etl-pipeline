# financial-ledger-etl-pipeline
An end-to-end Python and SQL data engineering pipeline transforming unstructured ledger data into a relational star-schema data warehouse.
# End-to-End Financial ETL Pipeline & Relational Data Warehouse

An automated data engineering solution designed to ingest, clean, and model unstructured regional financial ledger documents into an analytics-ready relational database framework.

## 🏗️ System Architecture
This project processes accounting data through a structured **Extract, Transform, Load (ETL)** pipeline, moving flat text data into an optimized **Star Schema**:

1. **Extract:** Programmatically streams raw, semicolon-delimited text assets containing regional columns and string formatting anomalies (`General_Ledger_Standard_Accounts_2_character.csv`).
2. **Transform:** A Python text-parsing pipeline (`clean_ledger.py`) strips text qualifiers, drops non-essential language columns, sanitizes whitespace, and outputs a clean text dimension table (`clean_accounts_lookup.csv`).
3. **Load:** An engineering script (`load_to_sql.py`) initializes a local SQLite relational data engine, programmatically instantiating database tables while enforcing primary and foreign key constraints.
4. **Data Aggregation & BI Reporting:** Granular financial journal entries are injected into a transaction fact table (`append_transactions.py`) and aggregated using multi-table relational SQL joins (`export_balance_report.py`) to generate executive-ready summary files.

## 💻 Tech Stack & Toolkit
* **Languages:** Python 3.x (Utilizing native `csv` and `sqlite3` engines)
* **Database Management System:** SQLite RDBMS
* **Analytics Layer:** Standard SQL ANSI (Multi-table `INNER JOIN`, column aggregations, and `GROUP BY` logic)

## 📊 Relational Database Design
To guarantee database integrity and prevent data anomalies, the target data warehouse implements a strict **One-to-Many (1:N)** star schema constraint:

* **`accounts_dim` (Dimension Table):** Stores unique, verified corporate account numbers and their standardized English descriptions.
* **`transactions_fact` (Fact Table):** Tracks granular operational business transactions (Dates, Debits, Credits) linked dynamically via a foreign key back to the account dimensions.

## 🚀 Execution Guide
To run the full data pipeline from scratch, execute the modules sequentially within a terminal environment:

```bash
# Phase 1: Sanitize and parse the raw flat files
python3 clean_ledger.py

# Phase 2: Provision relational database tables and load dimensions
python3 load_to_sql.py

# Phase 3: Inject operational ledger transactional metrics
python3 append_transactions.py

# Phase 4: Compute account balances and export executive business report
python3 export_balance_report.py
