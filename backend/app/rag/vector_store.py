from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy

from app.rag.embeddings import get_embeddings
from app.config import TOP_K


def build_vector_store(chunks):
    if not chunks:
        raise ValueError("Chunks cannot be empty when building vector store.")
    
    metadatas = [{"chunk_id": i} for i in range(len(chunks))]
    
    return FAISS.from_texts(
        texts = chunks,
        embedding=get_embeddings(),
        metadatas=metadatas,
        distance_strategy = DistanceStrategy.MAX_INNER_PRODUCT,
    )
    
    
def search_store(store,query,k=TOP_K):
    results = store.similarity_search_with_score(query, k=k)
    return [
        {
            "chunk_id": doc.metadata["chunk_id"],
            "text":doc.page_content,
            "score": float(score),
        }
        for doc, score in results
    ]