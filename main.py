
import csv
from pathlib import Path

from scanner.file_scanner import scan_documents

# ROOT_DIRECTORY = Path.home()
ROOT_DIRECTORY = Path.home() / "Documents" / "PersonalKnowledge"
OUTPUT_DIRECTORY = Path("output")
OUTPUT_FILE = OUTPUT_DIRECTORY / "document_inventory.csv"


def save_inventory(documents):
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)

    if not documents:
        print("No supported documents found.")
        return

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        fieldnames = documents[0].keys()

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(documents)


def main():
    print(f"Scanning: {ROOT_DIRECTORY}")
    print("This may take some time...")

    documents = scan_documents(ROOT_DIRECTORY)

    save_inventory(documents)

    print("\nScan completed!")
    print(f"Total documents discovered: {len(documents)}")
    print(f"Inventory saved at: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()
