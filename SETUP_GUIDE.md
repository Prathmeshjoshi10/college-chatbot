# College Chatbot Setup Guide

This guide will walk you through setting up and running the College Chatbot application.

## Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- Anthropic API key (for Claude 3.7 Sonnet)

## Step 1: Set Up the Backend

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the backend directory by copying the `.env.example` file:
   ```
   copy .env.example .env
   ```

6. Edit the `.env` file and add your Google API key:
   ```
   GOOGLE_API_KEY=AIzaSyDh_bB29TU_ge26Pke-E9LkOrQviWw6Ryo
   COLLEGE_NAME="Your College Name"
   ```

## Step 2: Prepare Your College Data

1. Add your college data files to the `backend/data/raw` directory. You can use various formats:
   - JSON files
   - Text files
   - CSV files
   - PDF files
   - Markdown files
   - HTML files

   A sample data file is provided at `backend/data/raw/sample_college_data.json`.

2. Process your data:
   ```
   cd ..
   python scripts/data_processing/process_data.py
   ```

3. Load the processed data into the vector database:
   ```
   python scripts/data_processing/load_vectordb.py
   ```

## Step 3: Start the Backend Server

1. Make sure you're in the backend directory and your virtual environment is activated.

2. Start the FastAPI server:
   ```
   uvicorn app.main:app --reload
   ```

   The backend server will run at `http://localhost:8000`.

## Step 4: Set Up the Frontend

1. Open a new terminal window and navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install the required packages:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

   The frontend will run at `http://localhost:3000`.

## Step 5: Use the Chatbot

1. Open your browser and go to `http://localhost:3000`.

2. Start asking questions about your college!

## Customizing the Chatbot

### Adding More Data

You can add more data files to the `backend/data/raw` directory at any time. After adding new files, run the data processing and vector database loading scripts again:

```
python scripts/data_processing/process_data.py
python scripts/data_processing/load_vectordb.py
```

### Customizing the Frontend

You can customize the frontend by editing the files in the `frontend` directory. The main page is at `frontend/pages/index.tsx`.

### Adjusting the RAG System

You can adjust the RAG system parameters in `backend/app/services/rag_service.py`. For example, you can change the number of retrieved documents, the chunk size, or the model parameters.

## Troubleshooting

### API Key Issues

If you see an error about the API key, make sure you've added your Anthropic API key to the `.env` file.

### Vector Database Issues

If you encounter issues with the vector database, try deleting the `backend/vectordb` directory and running the data processing scripts again.

### Frontend Connection Issues

If the frontend can't connect to the backend, make sure the backend server is running and check for any CORS issues in the browser console.
