from pathlib import Path


def extract_text_file(path: Path) -> list[dict]:

    content = path.read_text(
        encoding="utf-8",
        errors="replace"
    )

    results = []

    for line_number, line in enumerate(
        content.splitlines(),
        start=1
    ):

        text = line.strip()

        if text:
            results.append({
                "location_type": "line",
                "location_value": line_number,
                "text": text
            })

    return results