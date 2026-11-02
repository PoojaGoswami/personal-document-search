import json
import csv

from pathlib import Path

from chunking.chunker import chunk_document


BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = (
    BASE_DIR / "output" / "extracted_documents.jsonl"
)

OUTPUT_FILE = (
    BASE_DIR / "output" / "document_chunks.jsonl"
)

REPORT_FILE = (
    BASE_DIR / "output" / "chunking_report.csv"
)


def main():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Extraction file not found: {INPUT_FILE}"
        )

    total_documents = 0
    successful_documents = 0
    failed_documents = 0
    total_chunks = 0

    report = []

    print("Starting document chunking...")
    print(f"Input: {INPUT_FILE}")

    with INPUT_FILE.open("r", encoding="utf-8") as input_file:

        with OUTPUT_FILE.open( "w", encoding="utf-8") as output_file:

            for line in input_file:

                if not line.strip():
                    continue

                total_documents += 1

                try:

                    document = json.loads(line)

                    chunks = chunk_document(document)

                    for chunk in chunks:

                        output_file.write(
                            json.dumps(
                                chunk,
                                ensure_ascii=False
                            ) + "\n"
                        )

                    total_chunks += len(chunks)

                    successful_documents += 1

                    report.append({
                        "filename": document["filename"],
                        "document_id": document["document_id"],
                        "total_words": sum(
                            section["text"].count(" ") + 1
                            for section in document["sections"]
                            if section["text"].strip()
                        ),
                        "total_chunks": len(chunks),
                        "status": "success"
                    })

                    print(
                        f"[{total_documents}] "
                        f"{document['filename']} "
                        f"-> {len(chunks)} chunks"
                    )

                except Exception as error:

                    failed_documents += 1

                    print(f"Failed to chunk document: {error}")

                    report.append({
                        "filename": "",
                        "document_id": "",
                        "total_words": 0,
                        "total_chunks": 0,
                        "status": f"failed: {error}"
                    })

    with REPORT_FILE.open("w",newline="",encoding="utf-8") as report_file:

        fieldnames = [
            "filename",
            "document_id",
            "total_words",
            "total_chunks",
            "status"
        ]

        writer = csv.DictWriter(report_file,fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(report)

    print("\n========== CHUNKING SUMMARY ==========")

    print(f"Documents processed: {total_documents}")
    print(f"Successful: {successful_documents}")
    print(f"Failed: {failed_documents}")
    print(f"Total chunks generated: {total_chunks}")

    print(f"\nOutput: {OUTPUT_FILE}")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    main()