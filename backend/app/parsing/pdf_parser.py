from pathlib import Path

import pymupdf  # PyMuPDF

import pdfplumber


MIN_TEXT_LENGTH = 50

def extract_with_pymupdf(file_path):
    text_parts = []
    with pymupdf.open(str(file_path)) as doc:
        for page in doc:
            text_parts.append(page.get_text())
    return "\n".join(text_parts)



def extract_with_pdfplumber(file_path):
    text_parts = []
    with pdfplumber.open(str(file_path)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
    return "\n".join(text_parts)


def extract_text_from_pdf(file_path):
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} nahi mili.")
    
    if file_path.suffix.lower() != ".pdf":
        raise ValueError(f"File {file_path} PDF format mein nahi hai.") 
    
    text = extract_with_pymupdf(file_path)
    
    if len(text.strip()) < MIN_TEXT_LENGTH:
        text = extract_with_pdfplumber(file_path)
        
    if len(text.strip()) < MIN_TEXT_LENGTH:
        raise ValueError(f"PDF {file_path} se text extract nahi ho paya ya bahut chhota hai.")
    
    return text