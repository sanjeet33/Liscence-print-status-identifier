import os
import pdfplumber
import pandas as pd

# Define paths relative to your script execution directory
DATA_DIR = "./data"
OUTPUT_CSV = "license_dataset.csv"

all_records = []

# Iterate through every PDF in the data/ folder
for file_name in os.listdir(DATA_DIR):
    if file_name.endswith(".pdf"):
        pdf_path = os.path.join(DATA_DIR, file_name)
        print(f"Processing PDF: {file_name}...")
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_idx, page in enumerate(pdf.pages):
                    table = page.extract_table()
                    if table:
                        # Iterate through rows (skip header row on first page)
                        start_idx = 1 if page_idx == 0 else 0
                        for row in table[start_idx:]:
                            # Clean text inside table cells
                            cleaned_row = [str(cell).strip().replace('\n', ' ') if cell else "" for cell in row]
                            
                            # Filter out completely empty or bad rows
                            if any(cleaned_row):
                                # Tag source metadata for your dataset
                                source_office = "Thulobharyang, Kathmandu" if "Thulobharyang" in file_name else "Bagmati Transport Office"
                                all_records.append([
                                    cleaned_row[0] if len(cleaned_row) > 0 else "",  # S.N.
                                    cleaned_row[1] if len(cleaned_row) > 1 else "",  # Applicant Name / Details
                                    cleaned_row[2] if len(cleaned_row) > 2 else "",  # License Number
                                    cleaned_row[3] if len(cleaned_row) > 3 else "",  # Category / Ref No
                                    source_office,
                                    "Bagmati Province",
                                    "Available / Printed"
                                ])
        except Exception as e:
            print(f"Error parsing {file_name}: {e}")

# Map into DataFrame
columns = ["SN", "Applicant_Name", "License_Number", "Category", "Branch_Office", "Province", "Status"]
df = pd.DataFrame(all_records, columns=columns)

# Drop redundant internal table headers if extracted accidentally
df = df[df["License_Number"].str.lower() != "license no"]

# Save to CSV
df.to_csv(OUTPUT_CSV, index=False)
print(f"\nExtraction Complete! Saved {len(df)} records into '{OUTPUT_CSV}'.")
