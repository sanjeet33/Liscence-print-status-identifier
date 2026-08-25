# Driving License Print Status Identifier & Data Pipeline

An end-to-end data pipeline and web application designed to collect, structure, and visualize printed driving license records from various Transport Management Offices (TMO) under Bagmati Province, Nepal (including Thulobharyang, Radhe Radhe, Ekantakuna, and Chabahil).

Instead of manually checking individual PDFs or web notices published by the Department of Transport Management (DoTM), this application scrapes notice bulletins, standardizes applicant records, stores them in a relational database, and exposes them through an instant search dashboard.

---

## Key Features

* **Automated Web Scraping:** Downloads published notice lists and PDFs directly from regional DoTM/Bagmati web portals using `requests` and `BeautifulSoup`.
* **PDF Table Extraction & Ingestion:** Uses `pdfplumber` to extract structured tabular data (Applicant Name, License Number, Category, Office, Status) into tabular CSV format.
* **Relational Storage with Upsert Safety:** Migrates extracted data to a local PostgreSQL database (`dotm_db`). Employs a `UNIQUE` constraint on `License_Number` to ignore duplicate entries during re-ingestion.
* **Interactive Search Dashboard:** A user-friendly Streamlit web interface allowing applicants to search by License Number or Name to instantly check card print status and collection branches.

---

## Tech Stack

* **Language:** Python 3.12
* **Web Scraping:** `requests`, `beautifulsoup4`
* **Data Processing:** `pdfplumber`, `pandas`
* **Database & ORM:** PostgreSQL, `psycopg2-binary`, `SQLAlchemy`
* **Frontend Dashboard:** Streamlit

---

## Pipeline Architecture

```text
┌──────────────────────────────────────────────┐
│           DoTM / Bagmati Portals             │
│   (PDF Notices & Regional Office Portals)    │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│       Data Collection & Extraction           │
│    - BeautifulSoup (PDF Scraping)            │
│    - pdfplumber (Tabular Extraction)         │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│        PostgreSQL Database (dotm_db)         │
│     Table: bagmati_licenses (With UNIQUE)    │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│            Streamlit Dashboard               │
│      (Real-time License Search & UI)         │
└──────────────────────────────────────────────┘

```

---

**Prerequisites**
Ensure you have Python 3.10+ and PostgreSQL installed on your machine.

---

**Clone the Repository**
```
git clone https://github.com/sanjeet33/Liscence-print-status-identifier.git
cd Liscence-print-status-identifier
```

---

**Install Dependencies**
```
pip install -r requirements.txt
```
---

# Database Configuration
**1. Log into your PostgreSQL instance and create the database:**
```
CREATE DATABASE dotm_db;
CREATE USER name WITH PASSWORD 'my_secure_password';
GRANT ALL PRIVILEGES ON DATABASE dotm_db TO name;
```

**2.Ensure your database connection URI inside your scripts matches your local credentials:**
```
postgresql://name:my_secure_password@localhost:5432/dotm_db
```

---

