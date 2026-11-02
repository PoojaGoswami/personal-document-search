import hashlib
import re

from pathlib import Path

from extraction.parser import extract_document


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".md",
    ".pptx",
    ".xlsx",
}


def calculate_checksum(path: Path) -> str:

    sha256 = hashlib.sha256()

    with path.open("rb") as file:

        for block in iter(
            lambda: file.read(1024 * 1024),
            b""
        ):
            sha256.update(block)

    return sha256.hexdigest()


def clean_text(text: str) -> str:

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def extract_file(path: Path) -> dict:

    checksum = calculate_checksum(path)

    extracted_sections = extract_document(path)

    sections = []

    for section in extracted_sections:

        cleaned_text = clean_text(
            section["text"]
        )

        if not cleaned_text:
            continue

        sections.append({
            "location_type": section["location_type"],
            "location_value": section["location_value"],
            "text": cleaned_text
        })

    return {
        "document_id": checksum,
        "filename": path.name,
        "extension": path.suffix.lower(),
        "file_path": str(path.resolve()),
        "parent_folder": str(path.parent.resolve()),
        "file_size_bytes": path.stat().st_size,
        "checksum": checksum,
        "sections": sections,
        "total_sections": len(sections),
        "extraction_status": (
            "success" if sections else "empty"
        )
    }