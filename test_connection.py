
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")

if not all([NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE]):
    raise ValueError(
        "Missing Neo4j configuration. Check your .env file."
    )

def test_connection():
    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
    )

    try:
        driver.verify_connectivity()
        print("✅ Successfully connected to Neo4j Aura!")

        with driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(
                "RETURN 'Neo4j connection successful!' AS message"
            )
            print(result.single()["message"])

    except Exception as error:
        print(f"❌ Connection failed: {error}")
        raise

    finally:
        driver.close()


if __name__ == "__main__":
    test_connection()
