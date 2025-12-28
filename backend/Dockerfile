# Use a base image with ML libraries pre-installed
FROM python:3.11

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy minimal requirements
COPY requirements-minimal.txt .

# Install Python dependencies step by step to avoid conflicts
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-minimal.txt

# Copy application code
COPY app/ ./app/
COPY .env .env

# Create necessary directories
RUN mkdir -p data/raw data/processed vectordb

# Create sample data directly in the container
RUN echo '[\
  {\
    "content": "Sample College is a premier educational institution established in 1985, located at 123 College Avenue, Sample City. The college is dedicated to providing high-quality education in various fields and has grown to become a leading center for academic excellence and innovation.",\
    "metadata": {"source": "college_info", "type": "general"}\
  },\
  {\
    "content": "Admission requirements include: completed application form, high school transcripts, SAT/ACT scores, letters of recommendation, and personal statement. Application deadlines are April 15 for fall semester and November 15 for spring semester. Application fee is $50.",\
    "metadata": {"source": "admissions", "type": "requirements"}\
  },\
  {\
    "content": "Tuition fees: Undergraduate $25,000 per year, Graduate $30,000 per year. Additional costs: Housing $10,000 per year, Meal plan $5,000 per year, Books and supplies $1,200 per year.",\
    "metadata": {"source": "fees", "type": "financial"}\
  },\
  {\
    "content": "Scholarships available: Merit Scholarship up to $15,000 per year for GPA 3.5 or higher, Leadership Scholarship up to $10,000 per year for demonstrated leadership, Community Service Scholarship up to $8,000 per year for significant community service.",\
    "metadata": {"source": "scholarships", "type": "financial_aid"}\
  }\
]' > data/processed/processed_documents.json

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "app.main"]
