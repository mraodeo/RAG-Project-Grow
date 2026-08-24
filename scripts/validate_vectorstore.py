import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def main():
    print("Initializing embedding model (sentence-transformers/all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    persist_dir = os.path.join(".", "vectorstore", "chroma_db")
    collection_name = "mutual_fund_faq"
    
    print(f"Loading ChromaDB from {persist_dir}...")
    vectorstore = Chroma(
        persist_directory=persist_dir, 
        embedding_function=embeddings,
        collection_name=collection_name
    )
    
    test_queries = [
        "What is the expense ratio of HDFC Mid-Cap Fund?",
        "Exit load for HDFC ELSS Tax Saver Fund",
        "Minimum SIP amount for HDFC Small Cap Fund",
        "Benchmark index for HDFC Large Cap Fund",
        "What is the riskometer category of HDFC Gold ETF Fund of Fund?",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*50}")
        print(f"Query {i}: {query}")
        print(f"{'='*50}")
        
        # Search vectorstore
        results = vectorstore.similarity_search_with_score(query, k=3)
        
        for j, (doc, score) in enumerate(results, 1):
            print(f"\n--- Result {j} (Score: {score:.4f}) ---")
            print(f"Scheme: {doc.metadata.get('scheme_name', 'Unknown')}")
            print(f"URL: {doc.metadata.get('source_url', 'Unknown')}")
            # Print a snippet of the content
            snippet = doc.page_content.replace('\n', ' ')[:200]
            print(f"Content snippet: {snippet}...")

if __name__ == "__main__":
    main()
