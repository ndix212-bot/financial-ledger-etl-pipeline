import csv
import sqlite3

db_file = 'company_ledger.db'
report_file = 'trial_balance_summary.csv'

print("--- Generating Financial Trial Balance Report ---")

try:
    # Connect to your production data warehouse
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Run the granular account aggregation query
    cursor.execute("""
        SELECT 
            t.account_id,
            a.description_eng,
            SUM(t.debit) AS total_debits,
            SUM(t.credit) AS total_credits,
            (SUM(t.debit) - SUM(t.credit)) AS net_balance
        FROM transactions_fact t
        INNER JOIN accounts_dim a ON t.account_id = a.account_id
        GROUP BY t.account_id;
    """)
    
    report_rows = cursor.fetchall()
    
    # Write the calculated matrix out to a standard business report CSV
    with open(report_file, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        
        # Write headers
        writer.writerow(['AccountID', 'AccountDescription', 'TotalDebits', 'TotalCredits', 'NetBalance'])
        
        # Write rows
        writer.writerows(report_rows)
        
    conn.close()
    print(f"🎉 SUCCESS! Automated business ledger report saved to: {report_file}")

except Exception as e:
    print(f"❌ Reporting failure: {e}")