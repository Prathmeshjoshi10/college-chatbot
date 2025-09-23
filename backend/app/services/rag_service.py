import os
from typing import List, Dict, Tuple, Any, Optional
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.prompts import PromptTemplate

class RAGService:
    def __init__(self):
        """Initialize the RAG service with Google Gemini and ChromaDB"""
        # Load API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Initialize vector store
        self.vector_store_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "vectordb")
        
        # Check if vector store exists
        if not os.path.exists(self.vector_store_path):
            os.makedirs(self.vector_store_path, exist_ok=True)
            # If this is a new setup, we'll need to load documents later
            self.vector_store = None
            print("Vector store directory created. Please load documents.")
        else:
            try:
                # Try to load existing vector store
                self.vector_store = Chroma(
                    persist_directory=self.vector_store_path,
                    embedding_function=self.embeddings
                )
                print(f"Loaded vector store with {self.vector_store._collection.count()} documents")
            except Exception as e:
                print(f"Error loading vector store: {e}")
                self.vector_store = None
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.0-pro",
            google_api_key=api_key,
            temperature=0.2,
            max_output_tokens=1024
        )
        
        # Create custom prompt template
        self.qa_template = """
        You are a helpful assistant for {college_name}. You answer questions about the college based on the provided context.
        
        Context information is below:
        ---------------------
        {context}
        ---------------------
        
        Given the context information and not prior knowledge, answer the question: {question}
        
        If you don't know the answer based on the provided context, just say "I don't have enough information to answer this question." Don't try to make up an answer.
        
        Answer in a helpful, conversational tone. Be concise but informative.
        """
        
        # Initialize conversation chain if vector store is available
        if self.vector_store:
            self._initialize_chain()
    
    def _initialize_chain(self):
        """Initialize the conversation chain with the vector store"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        
        # Create prompt
        prompt = PromptTemplate(
            template=self.qa_template,
            input_variables=["context", "question"],
            partial_variables={"college_name": "Your College"}  # Replace with actual college name
        )
        
        # Create memory
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Create retrieval chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 5}
            ),
            memory=memory,
            combine_docs_chain_kwargs={"prompt": prompt}
        )
    
    async def load_documents(self, documents: List[Document]) -> None:
        """Load documents into the vector store"""
        if not documents:
            raise ValueError("No documents provided")
        
        # Create or update vector store
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.vector_store_path
        )
        
        # Persist the vector store
        self.vector_store.persist()
        
        # Initialize chain
        self._initialize_chain()
        
        print(f"Loaded {len(documents)} documents into vector store")
    
    async def generate_response(self, query: str, chat_history: List[Dict] = None) -> Tuple[str, List[Dict]]:
        """Generate a response to the user's query using RAG"""
        if not self.vector_store:
            return "The knowledge base hasn't been loaded yet. Please add college data first.", []
        
        if not self.chain:
            self._initialize_chain()
        
        # Format chat history if provided
        formatted_history = []
        if chat_history:
            for message in chat_history:
                if message.get("role") == "user":
                    formatted_history.append((message.get("content", ""), ""))
                elif message.get("role") == "assistant":
                    if formatted_history:
                        # Update the last user message with the assistant's response
                        last_user, _ = formatted_history[-1]
                        formatted_history[-1] = (last_user, message.get("content", ""))
        
        # Get relevant documents for citation
        docs = self.vector_store.similarity_search(query, k=3)
        sources = [{"content": doc.page_content, "metadata": doc.metadata} for doc in docs]
        
        # Generate response
        response = await self.chain.ainvoke({
            "question": query,
            "chat_history": formatted_history
        })
        
        return response["answer"], sources
