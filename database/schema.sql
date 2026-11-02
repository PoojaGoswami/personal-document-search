CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS document_chunks (

    chunk_id TEXT PRIMARY KEY,

    document_id TEXT NOT NULL,

    filename TEXT NOT NULL,

    file_path TEXT NOT NULL,

    parent_folder TEXT,

    extension TEXT,

    chunk_index INTEGER NOT NULL,

    content TEXT NOT NULL,

    word_count INTEGER,

    start_word INTEGER,

    end_word INTEGER,

    source_locations JSONB,

    embedding vector(768) NOT NULL,

    embedding_model TEXT NOT NULL,

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(document_id, chunk_index, embedding_model)
);


CREATE INDEX IF NOT EXISTS idx_document_chunks_document_id
ON document_chunks(document_id);


CREATE INDEX IF NOT EXISTS idx_document_chunks_filename
ON document_chunks(filename);


CREATE INDEX IF NOT EXISTS idx_document_chunks_embedding
ON document_chunks
USING hnsw (embedding vector_cosine_ops);