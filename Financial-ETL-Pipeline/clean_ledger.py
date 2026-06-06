import csv

input_file = 'raw_ledger.csv'
output_file = 'clean_accounts_lookup.csv'

print("--- Starting Data Transformation Pipeline ---")

try:
    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=';')
        
        # Extract the header row
        header = next(reader)
        new_header = ['AccountID', 'DescriptionENG']
        cleaned_rows = []
        
        for row in reader:
            # Only process rows that have the columns we need
            if len(row) >= 3:
                account_id = row[0].strip()
                # Remove stray quotation marks around the English text
                description_eng = row[2].replace('"', '').strip()
                cleaned_rows.append([account_id, description_eng])
                
    # Write out the clean, standard comma-separated CSV file
    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerow(new_header)
        writer.writerows(cleaned_rows)
        
    print(f"🎉 SUCCESS! Processed {len(cleaned_rows)} rows.")
    print(f"Pristine file saved as: {output_file}")

except FileNotFoundError:
    print(f"❌ Error: Could not find '{input_file}' in this folder.")