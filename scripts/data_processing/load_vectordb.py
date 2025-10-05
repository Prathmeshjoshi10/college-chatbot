import os
import sys
import json
import argparse
from typing import List

# Add the project root to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def load_processed_documents(input_file: str) -> List[Document]:
    """
    Load processed documents from JSON file
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    documents = []
    for item in data:
        doc = Document(
            page_content=item["content"],
            metadata=item["metadata"]
        )
        documents.append(doc)
    
    return documents

def create_vector_database(documents: List[Document], output_dir: str) -> None:
    """
    Create a FAISS vector database from documents
    """
    # Initialize embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Create FAISS vector store
    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the FAISS index
    faiss_index_path = os.path.join(output_dir, "faiss_index")
    vector_store.save_local(faiss_index_path)
    
    print(f"Created FAISS vector database with {len(documents)} documents at {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Load processed data into vector database")
    parser.add_argument("--input-file", type=str, default="backend/data/processed/processed_documents.json", 
                        help="JSON file containing processed documents")
    parser.add_argument("--output-dir", type=str, default="backend/vectordb", 
                        help="Directory to save vector database")
    
    args = parser.parse_args()
    
    print(f"Loading processed documents from {args.input_file}...")
    documents = load_processed_documents(args.input_file)
    print(f"Loaded {len(documents)} documents")
    
    print(f"Creating vector database at {args.output_dir}...")
    create_vector_database(documents, args.output_dir)
    
    print("Vector database creation complete!")

if __name__ == "__main__":
    main()
