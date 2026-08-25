import pandas as pd
from sqlalchemy import create_engine

# Database Connection String
# Format: postgresql://USER:PASSWORD@HOST:PORT/DATABASE_NAME
DATABASE_URL = "postgresql://sanjeet:national1358@localhost:5432/dotm_db"

try:
    # 1. Create database engine connection
    engine = create_engine(DATABASE_URL)
    
    # 2. Load the CSV created by your pdfplumber script
    csv_file = "bagmati_license_dataset.csv"
    df = pd.read_csv(csv_file)
    print(f"Loaded {len(df)} records from {csv_file}.")

    # 3. Write DataFrame directly into Postgres table 'bagmati_licenses'
    df.to_sql('bagmati_licenses', engine, if_exists='replace', index=False)
    
    print("SUCCESS: Data imported into PostgreSQL table 'bagmati_licenses'!")

except Exception as e:
    print(f"Error importing data: {e}")
