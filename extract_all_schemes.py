
import csv
import time
import requests
from bs4 import BeautifulSoup

INPUT_FILE = "schemes.csv"
OUTPUT_FILE = "scheme_details.csv"

HEADERS = {"User-Agent": "Mozilla/5.0"}

def extract_scheme(url):
    response = requests.get(
        url,
        timeout=30,
        headers=HEADERS,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for table in soup.find_all("table"):
        data = {}

        for row in table.find_all("tr"):
            cells = row.find_all(["th", "td"], recursive=False)

            if len(cells) >= 2:
                key = cells[0].get_text(" ", strip=True).rstrip(":")
                value = cells[1].get_text(" ", strip=True)

                if key and value:
                    data[key] = value

        if "Scheme Title/Name" in data:
            return data

    return {}


with open(INPUT_FILE, newline="", encoding="utf-8") as file:
    schemes = list(csv.DictReader(file))

all_schemes = []

for index, scheme in enumerate(schemes, start=1):
    print(f"[{index}/{len(schemes)}] {scheme['scheme_name']}")

    try:
        details = extract_scheme(scheme["detail_url"])

        record = {
            "scheme_name": details.get(
                "Scheme Title/Name",
                scheme["scheme_name"],
            ),
            "detail_url": scheme["detail_url"],
            "department": details.get("Concerned Department", ""),
            "organisation": details.get("Organisation Name", ""),
            "sponsored_by": details.get("Sponsered By", ""),
            "funding_pattern": details.get("Funding Pattern", ""),
            "beneficiaries": details.get("Beneficiaries", ""),
            "benefits": details.get("Types of Benefits", ""),
            "eligibility": details.get("Eligibility criteria", ""),
            "application_process": details.get("How To avail", ""),
            "description": details.get("Description", ""),
            "scheme_type": details.get("Scheme Type", ""),
        }

        all_schemes.append(record)

    except requests.RequestException as error:
        print(f"  Request failed: {error}")

    time.sleep(0.5)

if all_schemes:
    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=all_schemes[0].keys(),
        )
        writer.writeheader()
        writer.writerows(all_schemes)

print(f"\nSuccessfully extracted: {len(all_schemes)} schemes")
print(f"Saved to: {OUTPUT_FILE}")
