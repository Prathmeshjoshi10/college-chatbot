# College Chatbot

A chatbot application that answers questions about your college using Google Gemini LLM and RAG (Retrieval-Augmented Generation).

## Features

- Answer questions about college admissions, fees, courses, faculty, etc.
- Uses your own college data to provide accurate information
- Powered by Google Gemini LLM
- Implements RAG (Retrieval-Augmented Generation) for accurate responses

## Tech Stack

### Backend
- Python
- FastAPI
- Google Generative AI (Gemini)
- LangChain
- ChromaDB (Vector Database)
- Sentence Transformers

### Frontend
- Next.js
- Tailwind CSS

## Project Structure

```
college-chatbot/
├── backend/                # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core functionality
│   │   ├── models/         # Data models
│   │   └── services/       # Services
│   ├── data/               # College data
│   │   ├── raw/            # Raw data files
│   │   └── processed/      # Processed data
│   └── vectordb/           # Vector database files
├── frontend/               # Next.js frontend
│   ├── components/         # React components
│   ├── pages/              # Next.js pages
│   ├── public/             # Static assets
│   └── styles/             # CSS styles
└── scripts/                # Utility scripts
    └── data_processing/    # Data processing scripts
```

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 16+
- Google API key (already included in the setup)

### Backend Setup
1. Navigate to the backend directory
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your Google API key (already included in the setup)
6. Run the backend: `uvicorn app.main:app --reload`

### Frontend Setup
1. Navigate to the frontend directory
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`

## Usage

### Quick Start

The easiest way to run the application is to use the provided script:

```
python run_app.py
```

This script will:
1. Check and install required dependencies
2. Create the .env file with your Google API key
3. Process the sample college data
4. Start both the backend and frontend servers
5. Open the application in your browser

### Manual Setup

1. Add your college data to the `backend/data/raw` directory
2. Run the data processing script: `python scripts/data_processing/process_data.py`
3. Start the backend and frontend servers
4. Access the chatbot at `http://localhost:3000`

## License

MIT
