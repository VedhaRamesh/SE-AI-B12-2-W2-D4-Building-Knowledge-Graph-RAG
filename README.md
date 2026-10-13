# Scheme Navigator AI

A Streamlit-based knowledge-graph and Retrieval-Augmented Generation (RAG) application for exploring government schemes relevant to agriculture and rural development in Tamil Nadu. The project stores scheme metadata in Neo4j, maps relationships between departments, beneficiaries, and crops, and uses an LLM to answer natural-language questions grounded in the available scheme records.

## Overview

The system combines:

- A structured source dataset of government schemes
- Graph-based storage in Neo4j for relationships and filtering
- Semantic question answering using LangChain and OpenAI models
- A user-friendly Streamlit interface for browsing and asking questions

This makes it easier to search for scheme information by topic, crop, or department instead of manually reading a large spreadsheet or browsing multiple official pages.

## What the app does

- Searches schemes by keyword, such as a crop, benefit, or program name
- Filters schemes by crop relationships stored in the graph
- Returns relevant scheme details, funding patterns, and source links
- Uses an LLM to answer user questions while keeping responses grounded in the retrieved graph context
- Highlights uncertainty when a source is missing or a benefit is not clearly mapped

## Tech stack

- Python
- Streamlit for the interface
- Neo4j for the knowledge graph
- LangChain + OpenAI for the RAG layer
- Python dotenv for environment configuration
- CSV-based ingestion pipeline for scheme records

## Project structure

- `app.py` – Streamlit application UI and page configuration
- `query_graph.py` – Neo4j queries for keyword and crop-based scheme lookups
- `rag_answer.py` – LLM prompt and answer generation using retrieved context
- `import_schemes_to_neo4j.py` – imports scheme CSV records into Neo4j
- `create_graph.py` – creates a sample graph structure for testing
- `extract_schemes.py` and `extract_all_schemes.py` – scraping/extraction utilities
- `validate_schemes.py` – validation checks for scheme data quality
- `test_connection.py` – verifies Neo4j connectivity
- `scheme_details.csv` and `schemes.csv` – source data files
- `.env.example` – environment variable template

## Data flow

1. Scheme information is collected and stored in CSV files.
2. The data is imported into Neo4j with nodes such as `Department`, `Scheme`, `Crop`, and `Beneficiary`.
3. The UI or Python scripts query the graph for matching schemes.
4. The matching records are passed into the RAG prompt as context.
5. The model answers the user question while keeping responses constrained to the supplied context.

## Prerequisites

Before running the project, make sure you have:

- Python 3.10+ installed
- A Neo4j instance running locally or in Neo4j Aura
- An OpenAI API key with access to a supported chat model
- Internet access for the scraper/data collection utilities if you need to refresh sources

## Environment setup

Create a `.env` file in the project root using the example file as a template:

```bash
cp .env.example .env
```

Then set the required values:

```env
NEO4J_URI=neo4j+s://YOUR_INSTANCE_ID.databases.neo4j.io
NEO4J_USERNAME=YOUR_USERNAME
NEO4J_PASSWORD=YOUR_PASSWORD
NEO4J_DATABASE=YOUR_DATABASE
OPENAI_API_KEY=YOUR_OPENAI_KEY
```

If you are running a local Neo4j instance, the `NEO4J_URI` may look like:

```env
NEO4J_URI=bolt://localhost:7687
```

## Python dependencies

Install the project dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install streamlit python-dotenv neo4j langchain langchain-openai openai
```

If you prefer, you can also install additional packages required by the extraction scripts as needed, but the core application uses the packages above.

## Starting Neo4j

Make sure Neo4j is running before importing or querying the graph. If you are using a local Neo4j Desktop or Docker instance, confirm that the database is available and the credentials match your `.env` file.

## Loading graph data

To import the scheme dataset into Neo4j:

```bash
python import_schemes_to_neo4j.py
```

This script reads the CSV records and creates `Department` and `Scheme` nodes, then links them with `OFFERS` relationships.

You can also test the database connection:

```bash
python test_connection.py
```

## Running the app

Start the Streamlit interface:

```bash
streamlit run app.py
```

After the app starts, use the sidebar or search controls to ask questions such as:

- Which schemes support maize cultivation?
- What schemes are available for pulses in Tamil Nadu?
- Which department offers a scheme related to irrigation or livestock?
- What are the application and funding details for a specific scheme?

## Example queries

The project is designed around questions similar to:

- “Show me schemes for maize.”
- “Which government schemes help farmers growing groundnut?”
- “Which departments offer crop-related agricultural programs?”
- “What funding or benefits are available for a scheme connected to pulses?”

## Query and answer behavior

The graph layer is responsible for retrieving relevant records. The RAG layer then builds a prompt from those scheme records and asks the LLM to provide a concise answer with:

- relevant scheme names and departments
- supported benefits
- eligibility details only when present in the source
- uncertainty or missing information
- official source URLs

The code is intentionally conservative: if the available source does not clearly support a claim, the response notes that the information is not specified or unclear.

## Notes and cautions

- The data is only as reliable as the source records and the official scheme pages.
- The app is intended to support exploration, not replace official government guidance.
- Always verify current program rules, funding, and deadlines with the relevant department or official portal before acting on the information.

## Common troubleshooting

If the app cannot connect to Neo4j:

- verify the `NEO4J_URI`, `NEO4J_USERNAME`, and `NEO4J_PASSWORD` values in `.env`
- check that the Neo4j database is running
- confirm that the database name matches `NEO4J_DATABASE`

If the RAG answers are incomplete:

- check whether the graph has been loaded correctly
- verify your `OPENAI_API_KEY` is set in the environment
- test with a direct query against the database before asking the app to answer a question

## License

This project is intended for educational and research use in the context of government-scheme data exploration and knowledge-graph RAG demos.
