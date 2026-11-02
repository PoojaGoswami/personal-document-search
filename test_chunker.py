from chunking.chunker import chunk_document


document = {
    "document_id": "test123",
    "filename": "test.pdf",
    "file_path": "/Users/test/test.pdf",
    "parent_folder": "/Users/test",
    "extension": ".pdf",
    "sections": [
        {
            "location_type": "page",
            "location_value": 1,
            "text": " ".join(
                f"word{i}" for i in range(1, 351)
            )
        }
    ]
}

chunks = chunk_document(
    document,
    chunk_size=100,
    overlap=20
)

assert len(chunks) == 5

assert chunks[0]["word_count"] == 100

assert chunks[1]["word_count"] == 100

assert chunks[0]["content"].split()[-20:] == (
    chunks[1]["content"].split()[:20]
)

assert chunks[0]["source_locations"][0]["location_value"] == 1

print("All chunking tests passed!")