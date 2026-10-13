
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE")


def create_graph():
    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    try:
        with driver.session(database=DATABASE) as session:
            session.run("""
                MERGE (d:Department {name: 'Agriculture'})
                MERGE (s:Scheme {
                    name: 'Example Agriculture Scheme'
                })
                MERGE (d)-[:OFFERS]->(s)
            """)

            print("✅ Sample knowledge graph created!")

            result = session.run("""
                MATCH (d:Department)-[r:OFFERS]->(s:Scheme)
                RETURN d.name AS department,
                       type(r) AS relationship,
                       s.name AS scheme
            """)

            for record in result:
                print(
                    f"{record['department']} "
                    f"--{record['relationship']}--> "
                    f"{record['scheme']}"
                )

    finally:
        driver.close()


if __name__ == "__main__":
    create_graph()
