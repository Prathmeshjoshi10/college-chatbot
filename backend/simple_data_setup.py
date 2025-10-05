#!/usr/bin/env python3
"""
Simple script to process college data and create FAISS vector store
"""
import os
import json
from pathlib import Path

def create_sample_documents():
    """Create sample documents from the college data"""
    print("Creating sample documents...")
    
    # Sample college data as documents
    documents = [
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
        },
        {
            "content": "Scholarships available: Merit Scholarship up to $15,000 per year for GPA 3.5 or higher, Leadership Scholarship up to $10,000 per year for demonstrated leadership, Community Service Scholarship up to $8,000 per year for significant community service.",
            "metadata": {"source": "scholarships", "type": "financial_aid"}
        },
        {
            "content": "Academic programs include Computer Science, Business Administration, Engineering, Liberal Arts, and Sciences. The college offers both undergraduate and graduate degree programs with experienced faculty and modern facilities.",
            "metadata": {"source": "academics", "type": "programs"}
        },
        {
            "content": "Campus facilities include modern classrooms, laboratories, library, student center, dormitories, dining halls, sports facilities, and recreational areas. The campus provides a conducive environment for learning and personal growth.",
            "metadata": {"source": "facilities", "type": "campus"}
        }
    ]
    
    # Create processed directory
    processed_dir = Path("backend/data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Save processed documents
    output_file = processed_dir / "processed_documents.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Created {len(documents)} sample documents in {output_file}")
    return documents

def main():
    """Main function"""
    print("=== Simple Data Setup ===\n")
    
    # Create sample documents
    documents = create_sample_documents()
    
    print(f"\n✅ Setup complete! Created {len(documents)} documents.")
    print("You can now run the backend server with: python -m app.main")

if __name__ == "__main__":
    main()
