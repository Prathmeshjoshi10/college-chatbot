import os
import sys
import json
from dotenv import load_dotenv

# Add the project root to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.services.rag_service import RAGService
from langchain.schema import Document

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

def load_sample_data():
    """Load sample college data"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'data', 'raw', 'sample_college_data.json')
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convert data to documents
    documents = []
    
    # Process each section
    for section_key, section_data in data.items():
        if isinstance(section_data, dict):
            # Process nested dictionaries
            for subsection_key, subsection_data in section_data.items():
                if isinstance(subsection_data, dict):
                    # Handle nested dictionaries (2 levels deep)
                    content = f"{section_key} - {subsection_key}:\n"
                    content += json.dumps(subsection_data, indent=2)
                    metadata = {
                        "source": "sample_college_data.json",
                        "section": section_key,
                        "subsection": subsection_key
                    }
                    documents.append(Document(page_content=content, metadata=metadata))
                elif isinstance(subsection_data, list):
                    # Handle lists
                    content = f"{section_key} - {subsection_key}:\n"
                    content += "\n".join([f"- {item}" if isinstance(item, str) else json.dumps(item, indent=2) for item in subsection_data])
                    metadata = {
                        "source": "sample_college_data.json",
                        "section": section_key,
                        "subsection": subsection_key
                    }
                    documents.append(Document(page_content=content, metadata=metadata))
                else:
                    # Handle simple key-value pairs
                    content = f"{section_key} - {subsection_key}: {subsection_data}"
                    metadata = {
                        "source": "sample_college_data.json",
                        "section": section_key,
                        "subsection": subsection_key
                    }
                    documents.append(Document(page_content=content, metadata=metadata))
        elif isinstance(section_data, list):
            # Handle top-level lists
            content = f"{section_key}:\n"
            content += "\n".join([f"- {item}" if isinstance(item, str) else json.dumps(item, indent=2) for item in section_data])
            metadata = {
                "source": "sample_college_data.json",
                "section": section_key
            }
            documents.append(Document(page_content=content, metadata=metadata))
        else:
            # Handle simple top-level key-value pairs
            content = f"{section_key}: {section_data}"
            metadata = {
                "source": "sample_college_data.json",
                "section": section_key
            }
            documents.append(Document(page_content=content, metadata=metadata))
    
    return documents

async def main():
    # Initialize RAG service
    rag_service = RAGService()
    
    # Load and process sample data
    documents = load_sample_data()
    print(f"Loaded {len(documents)} documents from sample data")
    
    # Load documents into vector store
    await rag_service.load_documents(documents)
    
    # Test with a few sample questions
    test_questions = [
        "What is the tuition fee for undergraduate students?",
        "What are the admission requirements?",
        "Tell me about the campus housing options",
        "What scholarships are available?",
        "What is the student-faculty ratio?"
    ]
    
    for question in test_questions:
        print("\n" + "="*50)
        print(f"Question: {question}")
        response, sources = await rag_service.generate_response(question)
        print(f"Response: {response}")
        print("\nSources:")
        for i, source in enumerate(sources):
            print(f"Source {i+1}: {source['content'][:100]}...")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
