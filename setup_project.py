import os

# Define the project structure
directories = [
    "backend",
    "backend/app",
    "backend/app/api",
    "backend/app/core",
    "backend/app/models",
    "backend/app/services",
    "backend/data",
    "backend/data/raw",
    "backend/data/processed",
    "backend/vectordb",
    "frontend",
    "frontend/components",
    "frontend/pages",
    "frontend/public",
    "frontend/styles",
    "scripts",
    "scripts/data_processing"
]

# Create directories
for directory in directories:
    # Convert to Windows path format
    dir_path = os.path.join(*directory.split('/'))
    os.makedirs(dir_path, exist_ok=True)
    print(f"Created directory: {dir_path}")

print("Project structure setup complete!")
