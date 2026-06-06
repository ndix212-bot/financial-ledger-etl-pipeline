import csv
import sqlite3

csv_file = 'clean_accounts_lookup.csv'
db_file = 'company_ledger.db'

print("--- Initializing SQL Database Pipeline ---")

try:
    # Connect to SQLite (it will automatically create the file if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Drop tables if they exist to ensure a clean slate
    cursor.execute("DROP TABLE IF EXISTS transactions_fact;")
    cursor.execute("DROP TABLE IF EXISTS accounts_dim;")

    # Create tables
    cursor.execute("""
    CREATE TABLE accounts_dim (
        account_id INTEGER PRIMARY KEY,
        description_eng TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE transactions_fact (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        account_id INTEGER,
        debit REAL DEFAULT 0.0,
        credit REAL DEFAULT 0.0,
        FOREIGN KEY (account_id) REFERENCES accounts_dim(account_id)
    );
    """)
    print("✅ Relational database tables generated successfully.")

    # Read the clean CSV and insert data into our Dimension Table
    with open(csv_file, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader) # Skip the column headers
        
        row_count = 0
        for row in reader:
            if row:
                cursor.execute("INSERT INTO accounts_dim (account_id, description_eng) VALUES (?, ?);", (int(row[0]), row[1]))
                row_count += 1

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print(f"🎉 SUCCESS! Loaded {row_count} accounts into '{db_file}'.")

except FileNotFoundError:
    print(f"❌ Error: Could not find '{csv_file}'. Make sure Stage 1 was completed successfully.")