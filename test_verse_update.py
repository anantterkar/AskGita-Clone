#!/usr/bin/env python3
"""
Test script to verify the verse update system works correctly.
"""

import json
import datetime
import random

def test_daily_verses():
    """
    Test that different dates produce different verses.
    """
    print("Testing daily verse selection...")
    print("=" * 50)
    
    # Load all verses from verse.json
    with open('verse.json', 'r', encoding='utf-8') as f:
        verses = json.load(f)
    
    # Test a few different dates
    test_dates = [
        "2025-07-31",
        "2025-08-01", 
        "2025-08-02",
        "2025-08-03",
        "2025-08-04"
    ]
    
    verses_seen = set()
    
    for date_str in test_dates:
        # Use the date as a seed for consistent daily selection
        date_seed = int(date_str.replace('-', ''))
        random.seed(date_seed)
        
        # Select a random verse
        selected_verse = random.choice(verses)
        verses_seen.add(selected_verse['id'])
        
        print(f"Date: {date_str}")
        print(f"Verse ID: {selected_verse['id']}")
        print(f"Chapter: {selected_verse['chapter_number']}, Verse: {selected_verse['verse_number']}")
        print(f"Text: {selected_verse['text'][:50]}...")
        print("-" * 30)
    
    print(f"\nTotal unique verses selected: {len(verses_seen)}")
    print(f"Expected unique verses: {len(test_dates)}")
    
    if len(verses_seen) == len(test_dates):
        print("✅ SUCCESS: Each date produced a different verse!")
    else:
        print("❌ FAILED: Some dates produced the same verse.")
        print("This might happen occasionally due to random selection.")

def test_verse_format():
    """
    Test that the verse data has the correct format.
    """
    print("\nTesting verse data format...")
    print("=" * 50)
    
    # Test the actual update function
    from update_verse_of_day import get_verse_of_the_day
    verse_data = get_verse_of_the_day()
    
    required_fields = ['text', 'translation', 'verse_id', 'chapter_number', 'verse_number', 'transliteration', 'date']
    
    for field in required_fields:
        if field in verse_data:
            print(f"✅ {field}: Present")
        else:
            print(f"❌ {field}: Missing")
    
    # Check data types
    print(f"\nData type checks:")
    print(f"verse_id: {type(verse_data['verse_id'])} (should be int)")
    print(f"chapter_number: {type(verse_data['chapter_number'])} (should be int)")
    print(f"verse_number: {type(verse_data['verse_number'])} (should be int)")
    print(f"date: {type(verse_data['date'])} (should be str)")

if __name__ == "__main__":
    test_daily_verses()
    test_verse_format() 