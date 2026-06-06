import sqlite3
from datetime import datetime

db_file = 'company_ledger.db'

# Sample double-entry transaction batch to load into our Fact Table
mock_journal_entries = [
    # Format: (Date, AccountID, Debit, Credit)
    ('2026-06-01', 19, 15000.00, 0.00),    # Cash increase (Debit)
    ('2026-06-01', 30, 0.00, 15000.00),    # Sales Revenue increase (Credit)
    
    ('2026-06-02', 61, 450.00, 0.00),      # Freight Expense increase (Debit)
    ('2026-06-02', 19, 0.00, 450.00),      # Cash decrease (Credit)
    
    ('2026-06-03', 11, 50000.00, 0.00),    # Buildings asset increase (Debit)
    ('2026-06-03', 19, 0.00, 50000.00)     # Cash decrease (Credit)
]

print("--- Ingesting Transactional Fact Data ---")

try:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Enable foreign key support inside SQLite session
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Clear existing data to ensure clean iteration if re-run
    cursor.execute("DELETE FROM transactions_fact;")
    
    records_inserted = 0
    for record in mock_journal_entries:
        cursor.execute("""
            INSERT INTO transactions_fact (date, account_id, debit, credit)
            VALUES (?, ?, ?, ?);
        """, record)
        records_inserted += 1
        
    conn.commit()
    conn.close()
    print(f"🎉 SUCCESS! Processed and posted {records_inserted} transactional rows to the ledger fact table.")

except sqlite3.IntegrityError as e:
    print(f"❌ DATABASE INTEGRITY ERROR: Transaction rejected. Details: {e}")
except Exception as e:
    print(f"❌ Error encountered: {e}")