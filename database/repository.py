import json

from database.db import get_connection


def get_existing_chunk_ids(
    chunk_ids,
    embedding_model
):

    if not chunk_ids:
        return set()

    with get_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT chunk_id
                FROM document_chunks
                WHERE chunk_id = ANY(%s)
                  AND embedding_model = %s
                """,
                (
                    chunk_ids,
                    embedding_model
                )
            )

            return {
                row[0]
                for row in cursor.fetchall()
            }


def save_chunks(chunks, embeddings, embedding_model):

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Chunk and embedding counts do not match"
        )

    records = []

    for chunk, embedding in zip(chunks, embeddings):

        vector = "[" + ",".join(
            str(float(value))
            for value in embedding
        ) + "]"

        records.append((

            chunk["chunk_id"],

            chunk["document_id"],

            chunk["filename"],

            chunk["file_path"],

            chunk.get("parent_folder"),

            chunk.get("extension"),

            chunk["chunk_index"],

            chunk["content"],

            chunk.get("word_count"),

            chunk.get("start_word"),

            chunk.get("end_word"),

            json.dumps(
                chunk.get("source_locations", [])
            ),

            vector,

            embedding_model

        ))

    with get_connection() as conn:

        with conn.cursor() as cursor:

            cursor.executemany(

                """
                INSERT INTO document_chunks
                (
                    chunk_id,
                    document_id,
                    filename,
                    file_path,
                    parent_folder,
                    extension,
                    chunk_index,
                    content,
                    word_count,
                    start_word,
                    end_word,
                    source_locations,
                    embedding,
                    embedding_model
                )
                VALUES
                (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s::jsonb,
                    %s::vector, %s
                )
                ON CONFLICT (
                    document_id,
                    chunk_index,
                    embedding_model
                )
                DO UPDATE SET

                    chunk_id = EXCLUDED.chunk_id,

                    filename = EXCLUDED.filename,

                    file_path = EXCLUDED.file_path,

                    parent_folder = EXCLUDED.parent_folder,

                    extension = EXCLUDED.extension,

                    content = EXCLUDED.content,

                    word_count = EXCLUDED.word_count,

                    start_word = EXCLUDED.start_word,

                    end_word = EXCLUDED.end_word,

                    source_locations = EXCLUDED.source_locations,

                    embedding = EXCLUDED.embedding,

                    created_at = CURRENT_TIMESTAMP

                """,

                records

            )

    return len(records)