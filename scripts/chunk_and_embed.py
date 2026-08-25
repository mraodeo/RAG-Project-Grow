import os
import json
import glob
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# Mapping from slug to metadata
SCHEME_METADATA = {
    "hdfc_midcap": {"scheme_name": "HDFC Mid-Cap Fund Direct Growth", "category": "Mid-Cap"},
    "hdfc_smallcap": {"scheme_name": "HDFC Small Cap Fund Direct Growth", "category": "Small Cap"},
    "hdfc_gold_fof": {"scheme_name": "HDFC Gold ETF Fund of Fund Direct Plan Growth", "category": "Gold ETF FoF"},
    "hdfc_largecap": {"scheme_name": "HDFC Large Cap Fund Direct Growth", "category": "Large Cap"},
    "hdfc_elss": {"scheme_name": "HDFC ELSS Tax Saver Fund Direct Plan Growth", "category": "ELSS"}
}

def load_documents():
    docs = []
    proc_dir = os.path.join("data", "processed")
    raw_dir = os.path.join("data", "raw")
    
    for proc_file in glob.glob(os.path.join(proc_dir, "*.txt")):
        slug = os.path.basename(proc_file).replace(".txt", "")
        
        with open(proc_file, "r", encoding="utf-8") as f:
            text = f.read()
            
        # Try to read scrape metadata
        meta_file = os.path.join(raw_dir, slug, "metadata.json")
        source_url = ""
        last_updated = ""
        if os.path.exists(meta_file):
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
                source_url = meta.get("source_url", "")
                last_updated = meta.get("scrape_date", "")
                
        # Build metadata dictionary
        scheme_info = SCHEME_METADATA.get(slug, {})
        metadata = {
            "source_url": source_url,
            "scheme_name": scheme_info.get("scheme_name", slug),
            "category": scheme_info.get("category", "Unknown"),
            "last_updated": last_updated,
            "document_type": "scheme_page"
        }
        
        # Prepend the scheme name to the text to ensure LLM has context
        # in case a chunk gets separated from its source metadata
        text_with_context = f"Scheme: {metadata['scheme_name']}\n\n" + text
        
        docs.append(Document(page_content=text_with_context, metadata=metadata))
        print(f"Loaded {slug} ({len(text_with_context)} chars)")
        
    return docs

def main():
    print("Loading processed documents...")
    docs = load_documents()
    
    print("Splitting text into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n", " "]
    )
    
    chunked_docs = splitter.split_documents(docs)
    print(f"Generated {len(chunked_docs)} chunks in total.")
    
    print("Initializing embedding model (sentence-transformers/all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from src import config
    
    persist_dir = config.CHROMA_PERSIST_DIR
    collection_name = config.CHROMA_COLLECTION_NAME
    
    if os.path.exists(persist_dir):
        import shutil
        shutil.rmtree(persist_dir)
        print(f"Cleared existing ChromaDB at {persist_dir}")
    
    print(f"Indexing chunks into ChromaDB at {persist_dir}...")
    vectorstore = Chroma.from_documents(
        documents=chunked_docs,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name=collection_name
    )
    
    print("Done! ChromaDB is populated.")

if __name__ == "__main__":
    main()
