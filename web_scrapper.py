import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL for Bagmati DoTM Notices
TARGET_URL = "https://dotm.gov.np/content/53/regular-print-license-radheradhe/"
DOWNLOAD_DIR = "pdf_downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
}

def download_all_pdfs():
    print(f"Fetching notice page: {TARGET_URL}")
    response = requests.get(TARGET_URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to load page. Status: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all anchor tags ending in .pdf
    pdf_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.lower().endswith('.pdf'):
            full_url = urljoin(TARGET_URL, href)
            pdf_links.append(full_url)

    pdf_links = list(set(pdf_links)) # Remove duplicates
    print(f"Found {len(pdf_links)} PDF files to download.\n")

    for idx, url in enumerate(pdf_links, 1):
        filename = os.path.basename(url)
        # Clean filename
        filename = re.sub(r'[^\w\-_\. ]', '_', filename)
        save_path = os.path.join(DOWNLOAD_DIR, filename)

        if os.path.exists(save_path):
            print(f"[{idx}/{len(pdf_links)}] Already exists: {filename}")
            continue

        print(f"[{idx}/{len(pdf_links)}] Downloading {filename}...")
        try:
            res = requests.get(url, headers=headers, stream=True)
            with open(save_path, 'wb') as f:
                for chunk in res.iter_content(chunk_size=8192):
                    f.write(chunk)
        except Exception as e:
            print(f"Failed to download {url}: {e}")

    print("\nAll downloads completed!")

if __name__ == "__main__":
    download_all_pdfs()
