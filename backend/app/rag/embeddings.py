from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from app.config import EMBEDDING_MODEL

@lru_cache(maxsize=1)
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
        )

def embed_text(texts):
    if not texts:
        return []
    return get_embeddings().embed_documents(texts)


def embed_query(text):
    return get_embeddings().embed_query(text)