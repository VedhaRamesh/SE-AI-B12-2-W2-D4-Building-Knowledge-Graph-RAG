
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


def search_schemes_by_keyword(keyword):
    query = """
    MATCH (d:Department)-[:OFFERS]->(s:Scheme)
    WHERE toLower(coalesce(s.name, '')) CONTAINS toLower($keyword)
       OR toLower(coalesce(s.description, '')) CONTAINS toLower($keyword)

    RETURN d.name AS department,
        s.name AS scheme,
        s.funding_pattern AS funding,
        s.benefits_description AS benefits,
        s.description AS description,
        s.application_process AS application_process,
        s.source_url AS source_url

    ORDER BY
        CASE
            WHEN toLower(coalesce(s.name, '')) CONTAINS toLower($keyword)
            THEN 0
            ELSE 1
        END
    LIMIT 25
    """

    with GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    ) as driver:
        driver.verify_connectivity()

        records = driver.execute_query(
            query,
            keyword=keyword
        ).records

        return [record.data() for record in records]


def inspect_scheme_properties():
    """
    Display the labels and properties stored on Scheme nodes.
    This is a diagnostic function; it does not modify the graph.
    """
    query = """
    MATCH (s:Scheme)
    RETURN
        s.name AS scheme,
        labels(s) AS node_labels,
        keys(s) AS available_properties
    ORDER BY s.name
    LIMIT 10
    """

    with GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    ) as driver:
        driver.verify_connectivity()

        records = driver.execute_query(query).records

        print("\n🔍 Neo4j Scheme Node Inspection")
        print("=" * 60)

        for record in records:
            print(f"\nScheme: {record['scheme']}")
            print(f"Labels: {record['node_labels']}")
            print(f"Properties: {record['available_properties']}")


def inspect_graph_relationships():
    query = """
    MATCH (a)-[r]->(b)
    RETURN
        labels(a) AS source_labels,
        type(r) AS relationship,
        labels(b) AS target_labels,
        count(*) AS total
    ORDER BY total DESC
    """

    with GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    ) as driver:
        driver.verify_connectivity()

        records = driver.execute_query(query).records

        print("\n🔗 Neo4j Relationship Inspection")
        print("=" * 60)

        for record in records:
            print(
                f"{record['source_labels']} "
                f"-[:{record['relationship']}]-> "
                f"{record['target_labels']}: "
                f"{record['total']}"
            )

def inspect_crop_related_schemes():
    query = """
    MATCH (s:Scheme)
    WHERE
        toLower(s.name) CONTAINS 'maize'
        OR toLower(s.name) CONTAINS 'pulse'
        OR toLower(s.name) CONTAINS 'oilseed'
        OR toLower(s.name) CONTAINS 'groundnut'
        OR toLower(s.name) CONTAINS 'sesame'
    RETURN s.name AS scheme, s.source_url AS source_url
    ORDER BY s.name
    """

    with GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    ) as driver:
        driver.verify_connectivity()
        records = driver.execute_query(query).records

        print("\n🌾 Crop-Related Schemes")
        print("=" * 60)

        for record in records:
            print(f"\nScheme: {record['scheme']}")
            print(f"Source: {record['source_url']}")


def create_crop_relationships():
    query = """
    MATCH (s:Scheme)
    WITH s,
         toLower(coalesce(s.name, '')) AS scheme_name
    UNWIND [
        {crop: 'maize', keyword: 'maize'},
        {crop: 'pulses', keyword: 'pulses'},
        {crop: 'oilseeds', keyword: 'oilseed'},
        {crop: 'groundnut', keyword: 'groundnut'}
    ] AS crop_mapping
    WITH s, crop_mapping, scheme_name
    WHERE scheme_name CONTAINS crop_mapping.keyword
    MERGE (c:Crop {name: crop_mapping.crop})
    MERGE (s)-[:RELATED_TO_CROP]->(c)
    RETURN s.name AS scheme, c.name AS crop
    ORDER BY crop, scheme
    """

    with GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    ) as driver:
        driver.verify_connectivity()
        records = driver.execute_query(query).records

        print("\n🌾 Crop Relationships Created or Confirmed")
        print("=" * 60)

        for record in records:
            print(f"{record['crop']}: {record['scheme']}")

def search_schemes_by_crop(crop_name):
    query = """
    MATCH (d:Department)-[:OFFERS]->(s:Scheme)
          -[:RELATED_TO_CROP]->(c:Crop)
    WHERE toLower(c.name) CONTAINS toLower($crop_name)
    RETURN
        d.name AS department,
        s.name AS scheme,
        c.name AS crop,
        s.funding_pattern AS funding,
        s.benefits_description AS benefits,
        s.source_url AS source_url
    ORDER BY s.name
    """

    with GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    ) as driver:
        driver.verify_connectivity()
        records = driver.execute_query(
            query,
            crop_name=crop_name
        ).records

        print(f"\n🌾 Schemes related to {crop_name}")
        print("=" * 60)

        for record in records:
            print(f"\nScheme: {record['scheme']}")
            print(f"Crop: {record['crop']}")
            print(f"Department: {record['department']}")
            print(f"Financial Assistance: {record['funding'] or 'Not specified'}")
            print(f"Benefits: {record['benefits'] or 'Not specified'}")
            print(f"Source: {record['source_url']}")


def get_schemes_for_crop(crop_name):
    query = """
    MATCH (d:Department)-[:OFFERS]->(s:Scheme)
          -[:RELATED_TO_CROP]->(c:Crop)
    WHERE toLower(c.name) = toLower($crop_name)
    RETURN
        d.name AS department,
        s.name AS scheme,
        s.funding_pattern AS funding,
        s.benefits_description AS benefits,
        s.description AS description,
        s.application_process AS application_process,
        s.source_url AS source_url
    ORDER BY s.name
    """

    with GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    ) as driver:
        driver.verify_connectivity()
        records = driver.execute_query(
            query,
            crop_name=crop_name
        ).records

        return [dict(record) for record in records]

if __name__ == "__main__":
    search_schemes_by_crop("maize")
