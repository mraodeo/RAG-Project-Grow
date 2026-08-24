import os
import re
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from src import config

# Initialize embeddings and vectorstore once when module loads
print(f"[Retriever] Initializing embedding model: {config.EMBEDDING_MODEL}")
embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)

print(f"[Retriever] Connecting to ChromaDB at {config.CHROMA_PERSIST_DIR}")
vectorstore = Chroma(
    persist_directory=config.CHROMA_PERSIST_DIR,
    embedding_function=embeddings,
    collection_name=config.CHROMA_COLLECTION_NAME
)

# Mapping of keywords to scheme exact names (used in metadata)
SCHEME_ROUTING_MAP = {
    "mid cap": "HDFC Mid-Cap Fund Direct Growth",
    "small cap": "HDFC Small Cap Fund Direct Growth",
    "gold": "HDFC Gold ETF Fund of Fund Direct Plan Growth",
    "large cap": "HDFC Large Cap Fund Direct Growth",
    "elss": "HDFC ELSS Tax Saver Fund Direct Plan Growth",
    "tax saver": "HDFC ELSS Tax Saver Fund Direct Plan Growth"
}

def extract_scheme_filter(query: str) -> str | None:
    """
    Attempts to identify if the user is asking about a specific fund.
    Returns the exact scheme_name for metadata filtering, or None if broad query.
    """
    query_lower = query.lower()
    for keyword, exact_scheme_name in SCHEME_ROUTING_MAP.items():
        if keyword in query_lower:
            return exact_scheme_name
    return None

def retrieve(query: str, scheme_filter: str | None = None) -> list[dict]:
    """
    Retrieves the most relevant chunks for a given query.
    Implements MMR for diversity and explicit metadata filtering to prevent cross-contamination.
    """
    # 1. Metadata Filtering (Query Routing)
    if scheme_filter is None:
        scheme_filter = extract_scheme_filter(query)
        
    search_filter = None
    if scheme_filter:
        search_filter = {"scheme_name": scheme_filter}
        print(f"[Retriever] Applied hard filter: {search_filter}")

    # 2. Retrieval Execution
    results = []
    
    if config.RETRIEVAL_SEARCH_TYPE.lower() == "mmr":
        # MMR optimizes for relevance + diversity
        docs = vectorstore.max_marginal_relevance_search(
            query,
            k=config.RETRIEVAL_TOP_K,
            fetch_k=20, # Fetch more candidates to run MMR against
            filter=search_filter
        )
        # MMR doesn't return scores easily, so we just wrap the docs
        for doc in docs:
            results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": None
            })
    else:
        # Standard similarity search
        docs_and_scores = vectorstore.similarity_search_with_score(
            query,
            k=config.RETRIEVAL_TOP_K,
            filter=search_filter
        )
        for doc, score in docs_and_scores:
            results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score
            })
            
    return results

if __name__ == "__main__":
    # Quick test
    res = retrieve("What are the top holdings of the small cap fund?")
    print(f"Retrieved {len(res)} documents.")
    for r in res:
        print(f"-> {r['metadata'].get('scheme_name')}")
