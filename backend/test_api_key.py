#!/usr/bin/env python3
"""
Test script to verify Google API key works
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_api_key():
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # List available models
        print("\n📋 Listing available models...")
        models = genai.list_models()
        
        available_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model.name)
                print(f"  ✅ {model.name}")
        
        if not available_models:
            print("❌ No models support generateContent")
            return False
        
        # Test with the first available model
        model_name = available_models[0]
        print(f"\n🧪 Testing with model: {model_name}")
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello, can you say hi back?")
        
        print(f"✅ Test successful! Response: {response.text[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error testing API key: {e}")
        return False

if __name__ == "__main__":
    print("=== Google Gemini API Key Test ===\n")
    success = test_api_key()
    
    if success:
        print("\n🎉 API key is working correctly!")
    else:
        print("\n💡 Please check:")
        print("1. Your API key is correct")
        print("2. Your API key has proper permissions")
        print("3. Your .env file format is correct")
        print("4. You have internet connection")
