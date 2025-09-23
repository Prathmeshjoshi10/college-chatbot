import os
import sys
import json
import argparse
from typing import List, Dict, Any
import re

# Add the project root to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import (
    TextLoader,
    CSVLoader,
    PyPDFLoader,
    UnstructuredMarkdownLoader,
    UnstructuredHTMLLoader
)

def load_documents(data_dir: str) -> List[Document]:
    """
    Load documents from various file formats in the data directory
    """
    documents = []
    
    # Walk through the data directory
    for root, _, files in os.walk(data_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Process based on file extension
                if file.endswith('.txt'):
                    loader = TextLoader(file_path, encoding='utf-8')
                    documents.extend(loader.load())
                elif file.endswith('.csv'):
                    loader = CSVLoader(file_path)
                    documents.extend(loader.load())
                elif file.endswith('.pdf'):
                    loader = PyPDFLoader(file_path)
                    documents.extend(loader.load())
                elif file.endswith('.md'):
                    loader = UnstructuredMarkdownLoader(file_path)
                    documents.extend(loader.load())
                elif file.endswith('.html'):
                    loader = UnstructuredHTMLLoader(file_path)
                    documents.extend(loader.load())
                elif file.endswith('.json'):
                    # Custom handling for JSON files
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Process JSON data based on structure
                        if isinstance(data, list):
                            for item in data:
                                if isinstance(item, dict):
                                    content = json.dumps(item, ensure_ascii=False)
                                    metadata = {"source": file_path}
                                    documents.append(Document(page_content=content, metadata=metadata))
                        elif isinstance(data, dict):
                            # Extract key information from the dictionary
                            for key, value in data.items():
                                if isinstance(value, str):
                                    content = f"{key}: {value}"
                                    metadata = {"source": file_path, "key": key}
                                    documents.append(Document(page_content=content, metadata=metadata))
                                else:
                                    content = f"{key}: {json.dumps(value, ensure_ascii=False)}"
                                    metadata = {"source": file_path, "key": key}
                                    documents.append(Document(page_content=content, metadata=metadata))
                
                print(f"Loaded {file_path}")
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
    
    return documents

def split_documents(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Split documents into smaller chunks for better processing
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    
    return text_splitter.split_documents(documents)

def save_processed_documents(documents: List[Document], output_dir: str) -> None:
    """
    Save processed documents to JSON format
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert documents to a serializable format
    serialized_docs = []
    for i, doc in enumerate(documents):
        serialized_docs.append({
            "id": i,
            "content": doc.page_content,
            "metadata": doc.metadata
        })
    
    # Save to JSON file
    output_path = os.path.join(output_dir, "processed_documents.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(serialized_docs, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(serialized_docs)} processed documents to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Process college data for the chatbot")
    parser.add_argument("--data-dir", type=str, default="backend/data/raw", help="Directory containing raw data files")
    parser.add_argument("--output-dir", type=str, default="backend/data/processed", help="Directory to save processed data")
    parser.add_argument("--chunk-size", type=int, default=1000, help="Size of document chunks")
    parser.add_argument("--chunk-overlap", type=int, default=200, help="Overlap between document chunks")
    
    args = parser.parse_args()
    
    print(f"Loading documents from {args.data_dir}...")
    documents = load_documents(args.data_dir)
    print(f"Loaded {len(documents)} documents")
    
    print("Splitting documents...")
    split_docs = split_documents(documents, args.chunk_size, args.chunk_overlap)
    print(f"Split into {len(split_docs)} chunks")
    
    print(f"Saving processed documents to {args.output_dir}...")
    save_processed_documents(split_docs, args.output_dir)
    
    print("Processing complete!")

if __name__ == "__main__":
    main()
