import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://sanjeet:national1358@localhost:5432/dotm_db"

def search_license():
    try:
        engine = create_engine(DATABASE_URL)
        
        query_input = input("\nEnter License Number or Applicant Name to search: ").strip()
        
        # SQL query using parameterized ILIKE search for safety and case-insensitivity
        sql = """
            SELECT * FROM bagmati_licenses 
            WHERE "License_Number" ILIKE %s 
               OR "Applicant_Name" ILIKE %s
        """
        
        search_pattern = f"%{query_input}%"
        
        # Read matching records directly into a DataFrame
        df = pd.read_sql(sql, engine, params=(search_pattern, search_pattern))
        
        if not df.empty:
            print("\n================ RECORD FOUND ================")
            for idx, row in df.iterrows():
                print(f"License Number : {row.get('License_Number', 'N/A')}")
                print(f"Applicant Name : {row.get('Applicant_Name', 'N/A')}")
                print(f"Category       : {row.get('Category', 'N/A')}")
                print(f"Branch Office  : {row.get('Branch_Office', 'N/A')}")
                print(f"Status         : {row.get('Status', 'Available / Printed')}")
                print("----------------------------------------------")
            print(f"Total Matches Found: {len(df)}")
            print("================================================")
        else:
            print("\n================ NOT FOUND ================")
            print(f"No license record found matching: '{query_input}'")
            print("Status: License printing pending or details not found in Bagmati DB.")
            print("===========================================")
            
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    search_license()
