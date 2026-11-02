import json
from pathlib import Path
from collections import Counter

FILE = Path("output/extracted_documents.jsonl")

documents = []

with FILE.open(encoding="utf-8") as file:

    for line in file:
        documents.append(json.loads(line))


print("Total extracted documents:", len(documents))

print("\n--- Documents by extension ---")

print(
    Counter(doc["extension"] for doc in documents)
)

print("\n--- Total extracted sections ---")

print(
    sum(doc["total_sections"] for doc in documents)
)

print("\n--- Total extracted characters ---")

total_characters = sum(
    len(section["text"])
    for doc in documents
    for section in doc["sections"]
)

print(f"{total_characters:,}")

print("\n--- Sample document ---")

if documents:

    doc = documents[0]

    print("Filename:", doc["filename"])
    print("Location:", doc["file_path"])
    print("Sections:", doc["total_sections"])

    for section in doc["sections"][:3]:

        print("\nLocation:")
        print(section["location_type"])
        print(section["location_value"])

        print("\nText:")
        print(section["text"][:300])