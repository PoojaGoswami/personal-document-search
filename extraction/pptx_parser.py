from pathlib import Path
from pptx import Presentation


def extract_pptx(path: Path) -> list[dict]:

    presentation = Presentation(str(path))
    results = []

    for slide_number, slide in enumerate(
        presentation.slides,
        start=1
    ):

        slide_text = []

        for shape in slide.shapes:

            if shape.has_text_frame:
                text = shape.text.strip()

                if text:
                    slide_text.append(text)

            if shape.has_table:
                for row in shape.table.rows:
                    row_text = " | ".join(
                        cell.text.strip()
                        for cell in row.cells
                    )

                    if row_text.strip():
                        slide_text.append(row_text)

        combined_text = "\n".join(slide_text)

        if combined_text.strip():
            results.append({
                "location_type": "slide",
                "location_value": slide_number,
                "text": combined_text
            })

    return results