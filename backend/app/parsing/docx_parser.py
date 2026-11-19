from pathlib import Path

from docx import Document

MIN_TEXT_LENGTH = 50

def extract_paragraphs(doc):
    parts = []
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text:
            parts.append(text)
    return parts


def extract_tables(doc):
    parts = []
    for table in doc.tables:
        for row in table.rows:
            row_cells = []
            for cell in row.cells:
                cell_text = cell.text.strip()
                if cell_text and cell_text not in row_cells:
                    row_cells.append(cell_text)
            if row_cells:
                parts.append(" | ".join(row_cells))
    return parts


def extract_text_from_docx(file_path):
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} nahi mili.")

    if file_path.suffix.lower() != ".docx":
        raise ValueError(f"File {file_path} DOCX format mein nahi hai.")
    
    doc = Document(str(file_path))
    
    parts = extract_paragraphs(doc) + extract_tables(doc)
    text = "\n".join(parts)
    
    if len(text.strip()) < MIN_TEXT_LENGTH:
        raise ValueError(f"DOCX {file_path} se text extract nahi ho paya ya bahut chhota hai.")
    
    return text