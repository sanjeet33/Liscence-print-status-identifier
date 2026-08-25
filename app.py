import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Page Configuration
st.set_page_config(page_title="Bagmati License Verification Portal", page_icon="🇳🇵", layout="centered")

# Database Connection
DATABASE_URL = "postgresql://sanjeet:national1358@localhost:5432/dotm_db"

@st.cache_resource
def get_engine():
    return create_engine(DATABASE_URL)

st.title("🇳🇵 Bagmati License Status Verification")
st.write("Department of Transport Management (DoTM) — Bagmati Province Record Lookup")

# Search Bar Input
search_query = st.text_input("Enter Driving License Number or Applicant Name:", placeholder="e.g., 01-06-00123456 or Sanjeet")

if st.button("Check Status", type="primary"):
    if search_query.strip():
        try:
            engine = get_engine()
            sql = """
                SELECT * FROM bagmati_licenses 
                WHERE "License_Number" ILIKE %s 
                   OR "Applicant_Name" ILIKE %s
            """
            pattern = f"%{search_query.strip()}%"
            df = pd.read_sql(sql, engine, params=(pattern, pattern))

            if not df.empty:
                st.success(f"Record Found! ({len(df)} matching entry/entries)")
                for idx, row in df.iterrows():
                    with st.container():
                        st.subheader(f"👤 {row.get('Applicant_Name', 'N/A')}")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**License Number:** `{row.get('License_Number', 'N/A')}`")
                            st.write(f"**Category:** {row.get('Category', 'N/A')}")
                        with col2:
                            st.write(f"**Branch Office:** {row.get('Branch_Office', 'N/A')}")
                            st.write(f"**Province:** {row.get('Province', 'Bagmati Province')}")
                        
                        status = row.get('Status', 'Available / Printed')
                        st.info(f"**Current Status:** {status}")
                        st.divider()
            else:
                st.error(f"No license record found matching '{search_query}'.")
                st.warning("Status: License printing pending or details not yet dispatched to office.")
        except Exception as e:
            st.error(f"Database Connection Error: {e}")
    else:
        st.warning("Please enter a valid License Number or Name.")
