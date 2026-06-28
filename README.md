# Database Vectorization

Vectorize relational databases to make them usable by Large Language Models (LLMs).

## Motivation

Traditional databases are optimized for SQL queries, not semantic search.

This project extracts metadata from relational databases, transforms it into meaningful documents, generates embeddings, and stores them in a vector database.

The result is an AI-ready representation of any relational database.

---

## Features

- Extract schema automatically
- Read tables, columns and relationships
- Generate human-readable descriptions
- Create embeddings
- Store vectors in FAISS / ChromaDB / Pinecone
- Semantic search
- Metadata enrichment
- Incremental updates

---

## Architecture

Database
        │
        ▼
Schema Extraction
        │
        ▼
Document Generator
        │
        ▼
Embedding Model
        │
        ▼
Vector Database
        │
        ▼
LLM

---

## Example

Input

Table: CUSTOMER

Columns

- id
- first_name
- last_name
- email

Generated document

"The CUSTOMER table stores registered customers.
Each customer has a unique identifier, first name,
last name and email address."

Embedding

↓

Stored into ChromaDB

↓

User asks

"Show me customer information"

↓

The LLM retrieves the CUSTOMER table documentation.

---

## Roadmap

- [ ] SQL Server support
- [ ] PostgreSQL support
- [ ] Oracle support
- [ ] MySQL support
- [ ] Automatic documentation generation
- [ ] Relationship embeddings
- [ ] Data profiling
- [ ] Business glossary
- [ ] RAG integration
- [ ] MCP Server

---

## Future ideas

- Detect primary business entities
- Learn table importance
- Generate ER diagrams
- Natural language SQL
- AI-powered database documentation
- Data lineage
- Semantic schema matching

---

## License

MIT
