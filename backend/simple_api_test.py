#!/usr/bin/env python3
"""
Simple API key test without dependencies
"""
import os

def test_api_key():
    print("=== Simple API Key Test ===\n")
    
    # Check if .env file exists
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file found")
        
        # Read .env file manually
        with open(env_file, 'r') as f:
            content = f.read()
        
        print(f"📄 .env file content (first 200 chars):")
        print(content[:200])
        
        # Check for API key
        if "GOOGLE_API_KEY" in content:
            print("✅ GOOGLE_API_KEY found in .env file")
            
            # Extract the key
            for line in content.split('\n'):
                if line.startswith('GOOGLE_API_KEY'):
                    key_part = line.split('=', 1)
                    if len(key_part) == 2:
                        api_key = key_part[1].strip()
                        if api_key:
                            print(f"✅ API key value: {api_key[:10]}...{api_key[-4:]}")
                            print(f"📏 API key length: {len(api_key)} characters")
                            
                            # Basic validation
                            if len(api_key) < 20:
                                print("⚠️  API key seems too short")
                            elif api_key.startswith('your_') or api_key == 'your_google_api_key_here':
                                print("❌ API key is still the placeholder value")
                            else:
                                print("✅ API key format looks valid")
                        else:
                            print("❌ API key is empty")
                    break
        else:
            print("❌ GOOGLE_API_KEY not found in .env file")
    else:
        print("❌ .env file not found")
        print("💡 Create a .env file with: GOOGLE_API_KEY=your_actual_key")

if __name__ == "__main__":
    test_api_key()
