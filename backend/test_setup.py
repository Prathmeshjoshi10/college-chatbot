#!/usr/bin/env python3
"""
Simple test script to verify the setup is working
"""
import os
import sys
import json
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_imports():
    """Test that all required imports work"""
    print("Testing imports...")
    
    try:
        from langchain.schema import Document
        print("✅ LangChain imported successfully")
    except ImportError as e:
        print(f"❌ LangChain import failed: {e}")
        return False
    
    try:
        from langchain.embeddings import HuggingFaceEmbeddings
        print("✅ HuggingFace Embeddings imported successfully")
    except ImportError as e:
        print(f"❌ HuggingFace Embeddings import failed: {e}")
        return False
    
    try:
        from langchain.vectorstores import FAISS
        print("✅ FAISS imported successfully")
    except ImportError as e:
        print(f"❌ FAISS import failed: {e}")
        return False
    
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI imported successfully")
    except ImportError as e:
        print(f"❌ Google Generative AI import failed: {e}")
        return False
    
    return True

def test_data_loading():
    """Test loading the sample data"""
    print("\nTesting data loading...")
    
    data_path = Path("backend/data/raw/sample_college_data.json")
    if not data_path.exists():
        print(f"❌ Sample data file not found at {data_path}")
        return False
    
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Sample data loaded successfully ({len(data)} sections)")
        return True
    except Exception as e:
        print(f"❌ Failed to load sample data: {e}")
        return False

def test_environment():
    """Test environment variables"""
    print("\nTesting environment...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print("✅ GOOGLE_API_KEY found in environment")
        return True
    else:
        print("⚠️  GOOGLE_API_KEY not found - you'll need to set this")
        return False

def main():
    """Run all tests"""
    print("=== RAG Chatbot Setup Test ===\n")
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test data loading
    if not test_data_loading():
        all_passed = False
    
    # Test environment
    env_ok = test_environment()
    
    print("\n=== Test Results ===")
    if all_passed:
        print("✅ All critical tests passed!")
        if not env_ok:
            print("⚠️  Remember to set your GOOGLE_API_KEY in the .env file")
    else:
        print("❌ Some tests failed. Check the output above.")
    
    return all_passed

if __name__ == "__main__":
    main()
