import json
import os
from pathlib import Path

from dotenv import load_dotenv

from embeddings.embedder import (
    embed_chunks,
    MODEL,
    BATCH_SIZE
)

from database.repository import (
    get_existing_chunk_ids,
    save_chunks
)


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

INPUT_FILE = (
    BASE_DIR / "output" / "document_chunks.jsonl"
)

MAX_CHUNKS = int(os.getenv("MAX_CHUNKS", "20"))


def read_batches(file_path, batch_size, max_chunks=0):

    batch = []
    processed = 0

    with file_path.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            if not line.strip():
                continue

            if max_chunks and processed >= max_chunks:
                break

            batch.append(json.loads(line))
            processed += 1

            if len(batch) >= batch_size:

                yield batch
                batch = []

    if batch:
        yield batch



def main():

    if not INPUT_FILE.exists():

        raise FileNotFoundError(
            f"Chunk file not found: {INPUT_FILE}"
        )

    total_processed = 0
    total_skipped = 0
    total_failed = 0

    print("Starting embedding pipeline...")

    print("Model:", MODEL)

    print("Batch size:", BATCH_SIZE)

    print("Dimensions:", 768)

    
    for batch_number, chunks in enumerate(read_batches(INPUT_FILE, BATCH_SIZE, MAX_CHUNKS), start=1):

        try:

            chunk_ids = [chunk["chunk_id"] for chunk in chunks]

            existing_ids = get_existing_chunk_ids(chunk_ids, MODEL)

            new_chunks = [
                chunk
                for chunk in chunks
                if chunk["chunk_id"] not in existing_ids
            ]

            total_skipped += len(existing_ids)

            if not new_chunks:

                continue

            print(
                f"\nBatch {batch_number}: "
                f"Embedding {len(new_chunks)} chunks"
            )

            embeddings = embed_chunks(new_chunks)

            saved = save_chunks(
                new_chunks,
                embeddings,
                MODEL
            )

            total_processed += saved

            print(
                f"Successfully stored: {saved}"
            )

        except Exception as error:

            failed_count = len(new_chunks) if "new_chunks" in locals() else len(chunks)
            total_failed += failed_count

            print(f"Batch {batch_number} failed: {error}")

    print("\n========== EMBEDDING SUMMARY ==========")

    print("New chunks stored:", total_processed)

    print("Existing chunks skipped:", total_skipped)

    print("Failed chunks:", total_failed)


if __name__ == "__main__":
    main()