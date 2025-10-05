import os
import json
from typing import List, Dict, Tuple, Any, Optional
import google.generativeai as genai

class SimpleRAGService:
    def __init__(self):
        """Initialize the simple RAG service with Google Gemini only"""
        # Load API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize Gemini model with correct model names from your API
        try:
            # Try gemini-2.5-flash first (fast and reliable)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            print("Using gemini-2.5-flash model")
        except Exception as e:
            print(f"Error with gemini-2.5-flash: {e}")
            try:
                # Fallback to gemini-flash-latest
                self.model = genai.GenerativeModel('gemini-flash-latest')
                print("Using gemini-flash-latest model")
            except Exception as e2:
                print(f"Error with gemini-flash-latest: {e2}")
                try:
                    # Fallback to gemini-2.0-flash
                    self.model = genai.GenerativeModel('gemini-2.0-flash')
                    print("Using gemini-2.0-flash model")
                except Exception as e3:
                    print(f"Error with gemini-2.0-flash: {e3}")
                    raise ValueError("Could not initialize any Gemini model")
        
        # Load documents from processed data
        self.documents = self._load_documents()
        print(f"Loaded {len(self.documents)} documents for RAG")
    
    def _load_documents(self) -> List[Dict]:
        """Load documents from the processed data file"""
        try:
            data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                   "data", "processed", "processed_documents.json")
            
            if os.path.exists(data_path):
                with open(data_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Return default documents if file doesn't exist
                return [
                    {
                        "content": "Sample College is a premier educational institution established in 1985, located at 123 College Avenue, Sample City. The college is dedicated to providing high-quality education in various fields and has grown to become a leading center for academic excellence and innovation.",
                        "metadata": {"source": "college_info", "type": "general"}
                    },
                    {
                        "content": "Admission requirements include: completed application form, high school transcripts, SAT/ACT scores, letters of recommendation, and personal statement. Application deadlines are April 15 for fall semester and November 15 for spring semester. Application fee is $50.",
                        "metadata": {"source": "admissions", "type": "requirements"}
                    },
                    {
                        "content": "Tuition fees: Undergraduate $25,000 per year, Graduate $30,000 per year. Additional costs: Housing $10,000 per year, Meal plan $5,000 per year, Books and supplies $1,200 per year.",
                        "metadata": {"source": "fees", "type": "financial"}
                    }
                ]
        except Exception as e:
            print(f"Error loading documents: {e}")
            return []
    
    def _find_relevant_documents(self, query: str, k: int = 3) -> List[Dict]:
        """Simple keyword-based document retrieval"""
        query_lower = query.lower()
        scored_docs = []
        
        for doc in self.documents:
            content_lower = doc["content"].lower()
            # Simple scoring based on keyword matches
            score = 0
            query_words = query_lower.split()
            
            for word in query_words:
                if len(word) > 3:  # Only consider words longer than 3 characters
                    score += content_lower.count(word)
            
            if score > 0:
                scored_docs.append((score, doc))
        
        # Sort by score and return top k
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored_docs[:k]]
    
    async def generate_response(self, query: str, chat_history: List[Dict] = None) -> Tuple[str, List[Dict]]:
        """Generate a response to the user's query using simple RAG"""
        # Find relevant documents
        relevant_docs = self._find_relevant_documents(query)
        
        if not relevant_docs:
            return "I don't have enough information to answer this question about the college.", []
        
        # Create context from relevant documents
        context = "\n\n".join([doc["content"] for doc in relevant_docs])
        
        # Create prompt
        prompt = f"""
        You are a helpful assistant for Sample College. Answer the question based on the provided context.
        
        Context:
        {context}
        
        Question: {query}
        
        Please provide a helpful and accurate answer based only on the context provided. If the context doesn't contain enough information, say so.
        """
        
        try:
            # Generate response using Gemini directly
            response = self.model.generate_content(prompt)
            
            # Format sources
            sources = [{"content": doc["content"][:200] + "...", "metadata": doc["metadata"]} 
                      for doc in relevant_docs]
            
            return response.text, sources
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Sorry, I encountered an error while processing your question: {str(e)}", []
    
    async def load_documents(self, documents: List[Dict]) -> None:
        """Load new documents (for compatibility)"""
        self.documents = documents
        print(f"Loaded {len(self.documents)} new documents")
