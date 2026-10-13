
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

print("Page title:", soup.title.get_text(strip=True) if soup.title else "No title")

print("\nLinks containing 'scheme':")
for link in soup.find_all("a", href=True):
    text = link.get_text(" ", strip=True)
    href = link["href"]

    if "scheme" in (text + " " + href).lower():
        print(f"{text} -> {urljoin(response.url, href)}")

print("\nLinks containing 'department':")
for link in soup.find_all("a", href=True):
    text = link.get_text(" ", strip=True)
    href = link["href"]

    if "department" in (text + " " + href).lower():
        print(f"{text} -> {urljoin(response.url, href)}")

print("\nTables found:", len(soup.find_all("table")))
print("Page text preview:")
print(soup.get_text(" ", strip=True)[:1500])
