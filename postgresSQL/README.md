# Llama 3.2 RAG with PostgreSQL
## Overview

In this project, I am working on a simple RAG (Retrieval-Augmented Generation) using a PDF source. I am utilizing **Llama 3.2** as the model and the **nomic-embed-text** embedding model, along with postgreSQL as the database. The project is designed to be simple for llm with RAG technique can be used in a local environment.
## Requirements
- Python 3.8 or higher
- PostgreSQL 16
- Ollama
- Docker
- Docker Compose
- pgAdmin (optional, for database management)
## Installation

- Set up Docker environment through docker-compose.yml.
```
docker-compose up -d
```
- Get into the PostgreSQL through the terminal:
```
psql -d "postgres://postgres:password@localhost:5433/postgres"
```
 - After running the above command, you will be in the PostgreSQL shell.
    - Create vector extension and pgai:

```
CREATE EXTENSION IF NOT EXISTS ai CASCADE;
```
- Can use pgAdmin to connect to the PostgreSQL database.
    - Host: localhost
    - Port: 5433
    - User: postgres
    - Password: password

- Set up Ollama:
```
ollama pull llama3.2
ollama pull nomic-embed-text #For embedding model
```

- Run push_data.py to push the data into PostgreSQL:
```
python push_data.py -d <your_pdf_file>
```
    - The script will read the PDF file, split it into chunks, and push the data into the PostgreSQL database.
    - You can check the data in the database using pgAdmin or through the PostgreSQL shell.


- Run rag_run.py to run the RAG:
```
python rag_run.py
```
    - The script will run and you will type your query, the model will retrieve the relevant data from the PostgreSQL database and generate a response.
    - You can check the output in the terminal.