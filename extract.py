import csv
import json

from pathlib import Path

from extraction.extractor import (
    extract_file,
    SUPPORTED_EXTENSIONS
)


BASE_DIR = Path(__file__).resolve().parent

INVENTORY_FILE = (
    BASE_DIR / "output" / "document_inventory.csv"
)

OUTPUT_FILE = (
    BASE_DIR / "output" / "extracted_documents.jsonl"
)

REPORT_FILE = (
    BASE_DIR / "output" / "extraction_report.csv"
)


def load_inventory():

    with INVENTORY_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        return list(csv.DictReader(file))


def save_jsonl(documents):

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8"
    ) as file:

        for document in documents:

            file.write(
                json.dumps(
                    document,
                    ensure_ascii=False
                ) + "\n"
            )


def save_report(results):

    if not results:
        return

    with REPORT_FILE.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "filename",
                "file_path",
                "status",
                "sections",
                "error"
            ]
        )

        writer.writeheader()
        writer.writerows(results)


def main():

    inventory = load_inventory()

    print(f"Total files in inventory: {len(inventory)}")

    report = []

    success_count = 0
    empty_count = 0
    unsupported_count = 0
    failed_count = 0

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8"
    ) as output:

        for index, item in enumerate(inventory, start=1):

            path = Path(item["file_path"])

            print(
                f"\n[{index}/{len(inventory)}] "
                f"Processing: {path.name}"
            )

            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:

                unsupported_count += 1

                report.append({
                    "filename": path.name,
                    "file_path": str(path),
                    "status": "unsupported",
                    "sections": 0,
                    "error": "Unsupported file format"
                })

                continue

            try:

                if not path.is_file():
                    raise FileNotFoundError(
                        "File no longer exists"
                    )

                document = extract_file(path)

                output.write(
                    json.dumps(
                        document,
                        ensure_ascii=False
                    ) + "\n"
                )

                if document["extraction_status"] == "success":
                    success_count += 1
                else:
                    empty_count += 1

                report.append({
                    "filename": path.name,
                    "file_path": str(path),
                    "status": document["extraction_status"],
                    "sections": document["total_sections"],
                    "error": ""
                })

                print(
                    f"Extracted sections: "
                    f"{document['total_sections']}"
                )

            except Exception as error:

                failed_count += 1

                print(f"ERROR: {error}")

                report.append({
                    "filename": path.name,
                    "file_path": str(path),
                    "status": "failed",
                    "sections": 0,
                    "error": str(error)
                })

    save_report(report)

    print("\n========== EXTRACTION SUMMARY ==========")

    print(f"Inventory files: {len(inventory)}")
    print(f"Successful: {success_count}")
    print(f"Empty: {empty_count}")
    print(f"Unsupported: {unsupported_count}")
    print(f"Failed: {failed_count}")

    print(f"\nJSONL: {OUTPUT_FILE}")
    print(f"Report: {REPORT_FILE}")



if __name__ == "__main__":
    main()