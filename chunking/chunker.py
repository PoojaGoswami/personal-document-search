import hashlib
import re

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

def generate_chunk_id(document_id, chunk_index):
    value = f"{document_id}:{chunk_index}"

    return hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()


def chunk_document(document, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Combine extracted document sections into overlapping chunks.

    Every word retains its original source location.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")


    word_records = []

    # Step 1: Flatten document sections into word records.
    for section in document.get("sections", []):

        text = section.get("text", "").strip()

        if not text:
            continue

        location = {
            "location_type": section["location_type"],
            "location_value": section["location_value"]
        }

        words = re.findall(r"\S+", text)

        for word in words:
            word_records.append({
                "word": word,
                "location": location
            })

    if not word_records:
        return []


    # Step 2: Calculate chunk positions.

    step_size = chunk_size - overlap

    chunks = []

    start = 0
    chunk_index = 0

    total_words = len(word_records)

    while start < total_words:

        end = min(start + chunk_size, total_words)
        current_records = word_records[start:end]

        chunk_text = " ".join(record["word"] for record in current_records)

        # Step 3: Preserve unique source locations.
        source_locations = []

        seen_locations = set()

        for record in current_records:
            location = record["location"]
            location_key = (
                location["location_type"],
                str(location["location_value"])
            )

            if location_key not in seen_locations:
                seen_locations.add(location_key)

                source_locations.append(location)

        
        # Step 4: Create chunk metadata.
        chunks.append({
            "chunk_id": generate_chunk_id(document["document_id"],  chunk_index ),

            "document_id": document["document_id"],

            "filename": document["filename"],

            "file_path": document["file_path"],

            "parent_folder": document["parent_folder"],

            "extension": document["extension"],

            "chunk_index": chunk_index,

            "content": chunk_text,

            "word_count": len(current_records),

            "start_word": start,

            "end_word": end - 1,

            "source_locations": source_locations
        })

        chunk_index += 1

        # Stop when the end of the document is reached.
        if end == total_words:
            break

        start += step_size

    return chunks












