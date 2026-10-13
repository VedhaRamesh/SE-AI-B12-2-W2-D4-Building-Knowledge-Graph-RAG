
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="

response = requests.get(
    URL,
    timeout=30,
    headers={"User-Agent": "Mozilla/5.0"},
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

schemes = []
seen_urls = set()

for link in soup.find_all("a", href=True):
    name = link.get_text(" ", strip=True)
    detail_url = urljoin(response.url, link["href"])

    if (
        "scheme_details.php?id=" in detail_url
        and name
        and detail_url not in seen_urls
    ):
        schemes.append({
            "scheme_name": name,
            "detail_url": detail_url,
        })
        seen_urls.add(detail_url)

with open(
    "schemes.csv",
    "w",
    newline="",
    encoding="utf-8",
) as csvfile:
    writer = csv.DictWriter(
        csvfile,
        fieldnames=["scheme_name", "detail_url"],
    )
    writer.writeheader()
    writer.writerows(schemes)

print(f"Extracted {len(schemes)} scheme links.")
print("Saved to schemes.csv")

for scheme in schemes[:5]:
    print(scheme["scheme_name"], "->", scheme["detail_url"])
