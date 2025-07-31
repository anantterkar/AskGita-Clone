#!/usr/bin/env python3
"""
Simple test script to verify the API endpoints work correctly.
"""

import requests
import json

def test_update_verse_endpoint():
    """
    Test the manual verse update endpoint.
    """
    print("Testing /update-verse endpoint...")
    print("=" * 50)
    
    try:
        # Start the Flask app in the background (you'll need to do this manually)
        # For now, let's just test the endpoint structure
        
        url = "http://localhost:5000/update-verse"
        response = requests.post(url)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS: Verse updated successfully!")
            print(f"Verse ID: {data['verse']['verse_id']}")
            print(f"Chapter: {data['verse']['chapter_number']}, Verse: {data['verse']['verse_number']}")
            print(f"Date: {data['verse']['date']}")
        else:
            print(f"❌ FAILED: Status code {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Flask app not running. Start it with: python app.py")
        print("Then run this test again.")
    except Exception as e:
        print(f"❌ ERROR: {e}")

def test_askgita_endpoint():
    """
    Test the main askgita endpoint.
    """
    print("\nTesting /askgita endpoint...")
    print("=" * 50)
    
    try:
        url = "http://localhost:5000/askgita"
        response = requests.get(url)
        
        if response.status_code == 200:
            print("✅ SUCCESS: /askgita endpoint accessible!")
            print(f"Response length: {len(response.text)} characters")
        else:
            print(f"❌ FAILED: Status code {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Flask app not running. Start it with: python app.py")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_update_verse_endpoint()
    test_askgita_endpoint() 