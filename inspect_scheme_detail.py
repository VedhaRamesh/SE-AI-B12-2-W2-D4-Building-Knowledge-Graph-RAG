
import requests
from bs4 import BeautifulSoup

URL = "https://www.tn.gov.in/scheme_details.php?id=MTU2Ng=="

response = requests.get(
    URL,
    timeout=30,
    headers={"User-Agent": "Mozilla/5.0"},
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Find the table containing the scheme details.
for table in soup.find_all("table"):
    scheme_data = {}

    for row in table.find_all("tr"):
        cells = row.find_all(["th", "td"], recursive=False)

        if len(cells) >= 2:
            key = cells[0].get_text(" ", strip=True).rstrip(":")
            value = cells[1].get_text(" ", strip=True)

            if key and value:
                scheme_data[key] = value

    if "Scheme Title/Name" in scheme_data:
        print("\n--- Extracted Scheme Data ---")

        for key, value in scheme_data.items():
            print(f"{key}: {value}")

        break
else:
    print("Scheme details table not found.")
