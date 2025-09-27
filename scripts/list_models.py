import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv("backend/.env")

# Configure the client
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

# Try a simpler approach
try:
    print("Attempting to use gemini-pro model directly:")
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Hello, what models are available?")
    print("Success! The model works.")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error with gemini-pro: {e}")

# Try other model names
for model_name in ["gemini-1.5-pro", "gemini-1.0-pro", "gemini-flash"]:
    try:
        print(f"\nTrying {model_name}:")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello")
        print(f"Success with {model_name}!")
    except Exception as e:
        print(f"Error with {model_name}: {e}")