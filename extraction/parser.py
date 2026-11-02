from pathlib import Path

from extraction.pdf_parser import extract_pdf
from extraction.docx_parser import extract_docx
from extraction.text_parser import extract_text_file
from extraction.pptx_parser import extract_pptx
from extraction.excel_parser import extract_xlsx


PARSERS = {
    ".pdf": extract_pdf,
    ".docx": extract_docx,
    ".txt": extract_text_file,
    ".md": extract_text_file,
    ".pptx": extract_pptx,
    ".xlsx": extract_xlsx,
}


def extract_document(path: Path) -> list[dict]:

    extension = path.suffix.lower()

    parser = PARSERS.get(extension)

    if parser is None:
        raise ValueError(
            f"Unsupported document format: {extension}"
        )

    return parser(path)