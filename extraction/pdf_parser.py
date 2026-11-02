from pathlib import Path
from pypdf import PdfReader


def extract_pdf(path: Path) -> list[dict]:

    reader = PdfReader(str(path))
    results = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        if text.strip():
            results.append({
                "location_type": "page",
                "location_value": page_number,
                "text": text
            })

    return results