
import csv

FILE = "scheme_details.csv"

with open(FILE, newline="", encoding="utf-8") as file:
    schemes = list(csv.DictReader(file))

print("Total schemes:", len(schemes))

fields_to_check = [
    "scheme_name",
    "department",
    "funding_pattern",
    "beneficiaries",
    "benefits",
    "eligibility",
    "application_process",
    "description",
]

print("\n--- Field completeness ---")

for field in fields_to_check:
    filled = sum(
        1 for scheme in schemes
        if scheme.get(field, "").strip()
    )
    print(f"{field}: {filled}/{len(schemes)} populated")

print("\n--- First 3 schemes ---")

for scheme in schemes[:3]:
    print("\nScheme:", scheme["scheme_name"])
    print("Department:", scheme["department"] or "Missing")
    print("Beneficiaries:", scheme["beneficiaries"] or "Missing")
    print("Description:", (scheme["description"] or "Missing")[:200])
