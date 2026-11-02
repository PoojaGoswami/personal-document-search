import json

from pathlib import Path
from collections import Counter


FILE = Path("output/document_chunks.jsonl")


def main():

    if not FILE.exists():
        raise FileNotFoundError(FILE)

    total_chunks = 0
    total_words = 0

    documents = Counter()

    sample_chunks = []

    with FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            if not line.strip():
                continue

            chunk = json.loads(line)

            total_chunks += 1

            total_words += chunk["word_count"]

            documents[chunk["filename"]] += 1

            if len(sample_chunks) < 5:
                sample_chunks.append(chunk)

    print("\n========== CHUNK STATISTICS ==========")

    print("Total chunks:", total_chunks)

    print("Unique documents:", len(documents))

    print("Average words per chunk:", round(
        total_words / total_chunks, 2
    ) if total_chunks else 0)

    print("\n--- Top documents by chunk count ---")

    for filename, count in documents.most_common(10):

        print(filename, ":", count)

    print("\n========== SAMPLE CHUNKS ==========")

    for chunk in sample_chunks:

        print("\n--------------------------------")

        print("Filename:", chunk["filename"])

        print("Chunk ID:", chunk["chunk_id"])

        print("Chunk index:", chunk["chunk_index"])

        print("Word count:", chunk["word_count"])

        print("File path:", chunk["file_path"])

        print("Source locations:")

        for location in chunk["source_locations"]:
            print(
                location["location_type"],
                location["location_value"]
            )

        print("\nContent:")

        print(chunk["content"][:500])


if __name__ == "__main__":
    main()