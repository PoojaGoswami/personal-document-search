# Personal Document Search Engine

A Python-based semantic search engine that helps you find documents on your Mac using natural-language queries.

You don't need to remember the exact filename or folder location. Just describe what you remember about the document, its content, or its purpose, and the search engine retrieves relevant passages from your indexed documents.

## 1. Features

- Scan documents from a configured folder on macOS.
- Extract text from PDF, DOCX, TXT, Markdown, PPTX, XLSX and CSV files (subject to parser support).
- Split documents into smaller, overlapping chunks.
- Generate vector embeddings using Google's Gemini Embedding API.
- Store document chunks and embeddings in PostgreSQL with pgvector.
- Search documents using natural-language queries.
- Retrieve matching content, filename, full file path and source location.
- Rank results using vector similarity.

## 2. Architecture

```text
                Document Folder
                       |
                       v
                 Phase 1
                 File Scanner
                       |
                       v
                 Phase 2
               Text Extraction
                       |
                       v
                 Phase 3
                  Chunking
                       |
                       v
                 Phase 4
              Embedding Generation
                       |
                       v
              PostgreSQL + pgvector
                       |
                       v
                 Phase 5
               Semantic Search
                       |
                       v
                Search Results
          Filename | Path | Content
              Source Location
```

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Embedding model | Gemini Embedding 2 |
| Database | PostgreSQL 16 |
| Vector search | pgvector |
| Containerization | Docker |
| Database connector | Psycopg |
| Environment configuration | python-dotenv |

## 4. Project Structure

```text
personal-document-search/
│
├── scanner/
│   └── file_scanner.py
│
├── extraction/
│   └── document_extractor.py
│
├── chunking/
│   └── chunker.py
│
├── embeddings/
│   └── embedder.py
│
├── database/
│   ├── db.py
│   ├── repository.py
│   └── schema.sql
│
├── output/
│   ├── document_inventory.csv
│   ├── extracted_documents.jsonl
│   ├── document_chunks.jsonl
│   └── extraction_report.csv
│
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
├── embed.py
├── search.py
└── README.md
```

*The exact filenames may differ slightly depending on your implementation.*

## 5. Prerequisites

Install the following on your Mac:

- Python 3
- Docker Desktop
- Google Gemini API key
- Git (optional)

Verify Python:

```bash
python3 --version
```

Verify Docker:

```bash
docker --version
docker compose version
```

## 6. Installation and Setup

### Step 1: Clone or navigate to the project

```bash
cd personal-document-search
```

### Step 2: Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip3 install -r requirements.txt
```

### Step 4: Configure environment variables

Create a `.env` file in the project root.

```env
# Gemini API
GEMINI_API_KEY=your_gemini_api_key
GEMINI_EMBEDDING_MODEL=gemini-embedding-2
EMBEDDING_DIMENSIONS=768

# PostgreSQL
DB_HOST=localhost
DB_PORT=5433
DB_NAME=document_search
DB_USER=docsearch
DB_PASSWORD=change_this_password

# Initial embedding limit
MAX_CHUNKS=20

# Optional: configure the scanner's allowed root folder
DOCUMENT_SCAN_ROOT=/Users/your_username/Documents/PersonalKnowledge
```

Replace the example values with your actual configuration.

**Important:** Ensure your scanner actually reads `DOCUMENT_SCAN_ROOT` before relying on this setting. Do not use the entire home directory as the scan root unless that is intentional.

### Step 5: Start PostgreSQL using Docker

```bash
docker compose up -d
```

Verify that the container is running:

```bash
docker ps
```

You should see:

```text
document-search-db
```

### Step 6: Initialize the database

```bash
python3 test_db.py
```

This should test the PostgreSQL connection and initialize the schema, including the pgvector extension.

## 7. Document Indexing Workflow

Run the following phases in order.

### Phase 1: Scan documents

```bash
python3 scanner/file_scanner.py
```

The scanner discovers supported documents in the configured folder.

Output:

```text
output/document_inventory.csv
```

### Phase 2: Extract document text

```bash
python3 extract.py
```

Extracts document content and source-location metadata.

Output:

```text
output/extracted_documents.jsonl
```

### Phase 3: Generate chunks

```bash
python3 chunk.py
```

Splits extracted text into smaller chunks with overlapping content.

Output:

```text
output/document_chunks.jsonl
```

### Phase 4: Generate embeddings and store them

For initial testing, configure:

```env
MAX_CHUNKS=20
```

Run:

```bash
python3 embed.py
```

After validating the initial embeddings, change:

```env
MAX_CHUNKS=0
```

Run the script again to process all remaining chunks.

**Note:** Zero means unlimited processing in the current implementation.

### Verify indexed documents

Connect to PostgreSQL:

```bash
docker exec -it document-search-db psql -U docsearch -d document_search
```

Check the number of indexed chunks:

```sql
SELECT COUNT(*) FROM document_chunks;
```

Check the number of unique documents:

```sql
SELECT COUNT(DISTINCT document_id)
FROM document_chunks;
```

Check embedding dimensions:

```sql
SELECT vector_dims(embedding), COUNT(*)
FROM document_chunks
GROUP BY vector_dims(embedding);
```

Exit PostgreSQL:

```sql
\q
```

## 8. Searching Documents

Once documents have been indexed, you can search using natural language.

### Basic command

```bash
python3 search.py "YOUR SEARCH QUERY"
```

### Return more results

```bash
python3 search.py "YOUR SEARCH QUERY" --top-k 10
```

The default number of results is 5.

## 9. Example Search Prompts

You can use the following commands directly in your terminal.

### A. Search by document content

Find a document based on something you remember reading inside it.

```bash
python3 search.py "Find the document where I wrote about configuring AWS Lambda reserved concurrency and throttling."
```

```bash
python3 search.py "Find documents containing information about AssumeRole, temporary security credentials and cross-account access."
```

### B. Search by topic or technology

Find documents based on a technology or subject.

```bash
python3 search.py "Find my notes about Snowflake Cortex Agent, RAG architecture and retrieval."
```

```bash
python3 search.py "Find documents explaining Terraform modules for deploying AWS infrastructure."
```

### C. Search by purpose

Describe what the document was created for.

```bash
python3 search.py "Find the document where I prepared interview questions about Snowflake performance optimization."
```

```bash
python3 search.py "Find the notes I created for preparing AWS Solutions Architect certification."
```

### D. Search using incomplete or remembered sentences

You don't need to remember the exact sentence.

```bash
python3 search.py "Find the document where I wrote something about Lambda execution environments being reused across invocations."
```

```bash
python3 search.py "Find the document where I mentioned that database connection pooling helps avoid creating a new connection for every request."
```

### E. Search by technical implementation or configuration

Useful when you remember a particular implementation detail.

```bash
python3 search.py "Find the document containing steps for configuring AWS Glue with Snowflake."
```

```bash
python3 search.py "Find my Terraform configuration examples for creating AWS Lambda functions with IAM roles."
```

### F. Search by approximate filename or document description

```bash
python3 search.py "Find my AWS interview preparation notes. I don't remember the filename or folder."
```

```bash
python3 search.py "Find the document where I documented my data pipeline architecture using S3, Kafka, Glue and Snowflake."
```

### G. Search with more results

```bash
python3 search.py "Find documents related to AWS networking, VPC, subnets, route tables and security groups." --top-k 10
```

```bash
python3 search.py "Find all my notes about Python decorators, generators and multithreading." --top-k 15
```

## 10. Understanding Search Results

A typical result contains:

| Field | Description |
|---|---|
| Filename | Original document name |
| Extension | PDF, DOCX, TXT, etc. |
| Similarity | Vector similarity score |
| Chunk | Matching chunk index |
| File path | Absolute path of the original document |
| Source location | Page, paragraph or other location |
| Content | Relevant extracted text |

Similarity scores help rank the results. A higher score generally indicates a closer vector match, but it does not guarantee that the result is relevant.

## 11. Useful Database and Docker Commands

| Command | Purpose |
|---|---|
| `docker ps` | List running containers |
| `docker compose up -d` | Start PostgreSQL |
| `docker compose stop` | Stop PostgreSQL |
| `docker compose start` | Restart stopped services |
| `docker compose logs postgres` | View database logs |
| `docker compose down` | Remove containers and networks |
| `docker volume ls` | List Docker volumes |

**Warning:** Avoid `docker compose down -v` unless you intentionally want to delete the database volume and its stored data.

## 12. Security and Privacy

This project may index personal documents, so privacy is important.

- Restrict scanning to a dedicated folder rather than the entire Mac home directory.
- Do not index financial records, identity documents, medical records or confidential work documents unless you have explicitly decided to do so.
- Keep `.env` out of Git.
- Never commit API keys or database passwords.
- Bind the PostgreSQL host port to localhost:

```yaml
ports:
  - "127.0.0.1:5433:5432"
```

- Remember that the current Gemini embedding implementation sends document text to Google's API.
- Review the applicable Google API data-handling terms before submitting personal or confidential information.
- Consider switching to local embeddings if you want document text to remain on your Mac.

## 13. Future Improvements

Planned enhancements:

- Hybrid search combining semantic and keyword retrieval.
- Document-level grouping to avoid duplicate results for multiple matching chunks.
- Better ranking and relevance thresholds.
- Search filters for file type, folder and modification date.
- Open the original document directly from search results.
- Local embedding models for stronger privacy.
- Automatic indexing when new documents are added.
- A simple web-based user interface.
- RAG-based question answering using retrieved document content.

---

## Quick Start

After the initial indexing is complete, you only need:

```bash
cd personal-document-search

source .venv/bin/activate

docker compose up -d

python3 search.py "Find the document where I wrote about AWS Lambda concurrency and throttling."
```

**Project goal:** Build a private, intelligent search engine that helps users find their own documents using the context they remember, even when they have forgotten the original filename or storage location.