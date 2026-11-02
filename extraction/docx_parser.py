from pathlib import Path
from docx import Document


def extract_docx(path: Path) -> list[dict]:

    document = Document(str(path))
    results = []

    for index, paragraph in enumerate(
        document.paragraphs,
        start=1
    ):

        text = paragraph.text.strip()

        if text:
            results.append({
                "location_type": "paragraph",
                "location_value": index,
                "text": text
            })

    # Extract tables as well.
    for table_index, table in enumerate(
        document.tables,
        start=1
    ):

        for row_index, row in enumerate(
            table.rows,
            start=1
        ):

            text = " | ".join(
                cell.text.strip()
                for cell in row.cells
            )

            if text.strip():
                results.append({
                    "location_type": "table_row",
                    "location_value": f"{table_index}:{row_index}",
                    "text": text
                })

    return results