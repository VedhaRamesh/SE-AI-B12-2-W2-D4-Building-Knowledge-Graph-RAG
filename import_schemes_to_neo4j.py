
import csv
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

if not all([URI, USERNAME, PASSWORD]):
    raise ValueError(
        "Please check NEO4J_URI, NEO4J_USERNAME, "
        "and NEO4J_PASSWORD in your .env file."
    )

def clean(value):
    return (value or "").strip()

with open(
    "scheme_details.csv",
    newline="",
    encoding="utf-8",
) as file:
    schemes = list(csv.DictReader(file))

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD),
)

query = """
MERGE (d:Department {name: $department})

MERGE (s:Scheme {name: $scheme_name})
SET s.funding_pattern = $funding_pattern,
    s.benefits_description = $benefits,
    s.description = $description,
    s.application_process = $application_process,
    s.scheme_type = $scheme_type,
    s.source_url = $detail_url

MERGE (d)-[:OFFERS]->(s)

WITH s, $beneficiaries AS beneficiary_name,
     $benefits AS benefit_name

FOREACH (_ IN CASE
    WHEN beneficiary_name <> '' THEN [1]
    ELSE []
END |
    MERGE (b:Beneficiary {name: beneficiary_name})
    MERGE (s)-[:FOR_BENEFICIARY]->(b)
)

FOREACH (_ IN CASE
    WHEN benefit_name <> '' THEN [1]
    ELSE []
END |
    MERGE (bt:Benefit {name: benefit_name})
    MERGE (s)-[:PROVIDES]->(bt)
)
"""

try:
    with driver.session() as session:
        for scheme in schemes:
            session.run(
                query,
                department=clean(scheme.get("department")),
                scheme_name=clean(scheme.get("scheme_name")),
                funding_pattern=clean(scheme.get("funding_pattern")),
                benefits=clean(scheme.get("benefits")),
                description=clean(scheme.get("description")),
                application_process=clean(
                    scheme.get("application_process")
                ),
                scheme_type=clean(scheme.get("scheme_type")),
                detail_url=clean(scheme.get("detail_url")),
                beneficiaries=clean(scheme.get("beneficiaries")),
            ).consume()

    print(f"Imported {len(schemes)} scheme records into Neo4j.")

finally:
    driver.close()
