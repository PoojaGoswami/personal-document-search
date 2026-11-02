from pathlib import Path
from openpyxl import load_workbook


def extract_xlsx(path: Path) -> list[dict]:

    workbook = load_workbook(
        filename=str(path),
        read_only=True,
        data_only=True
    )

    results = []

    try:
        for worksheet in workbook.worksheets:

            for row_number, row in enumerate(
                worksheet.iter_rows(values_only=True),
                start=1
            ):

                values = [
                    f"Column {index + 1}: {value}"
                    for index, value in enumerate(row)
                    if value is not None
                    and str(value).strip()
                ]

                if not values:
                    continue

                results.append({
                    "location_type": "sheet_row",
                    "location_value": (
                        f"{worksheet.title}:{row_number}"
                    ),
                    "text": " | ".join(values)
                })

    finally:
        workbook.close()

    return results