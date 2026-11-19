from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import CHUNK_SIZE, CHUNK_OVERLAP

def get_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
    )
    
def split_resume(text):
    if not text or not text.strip():
        return []
    
    
    splitter = get_splitter()
    chunks = splitter.split_text(text)
    return [chunk.strip() for chunk in chunks if chunk.strip()]