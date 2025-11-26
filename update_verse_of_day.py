import json
import datetime
import random
import csv

def get_verse_of_the_day():
    """
    Get a verse for today based on the current date.
    Uses the date as a seed for consistent daily selection.
    """
    # Load all verses from verse.json
    with open('verse.json', 'r', encoding='utf-8') as f:
        verses = json.load(f)
    
    # Load English translations from CSV
    translations_map = {}
    with open('gita_verses_translations.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            translations_map[int(row['verse_id'])] = row['description']
    
    # Get today's date as a string (YYYY-MM-DD)
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    # Use the date as a seed for consistent daily selection
    # Convert date string to a number for seeding
    date_seed = int(today.replace('-', ''))
    random.seed(date_seed)
    
    # Select a random verse
    selected_verse = random.choice(verses)
    
    # Format the verse data for verse_of_the_day.json
    verse_data = {
        "text": selected_verse["text"].strip(),
        "transliteration": selected_verse.get("transliteration", "").strip(),
        "word_meanings": selected_verse.get("word_meanings", "").strip(),
        "translation": translations_map.get(selected_verse["id"], "").strip(),
        "verse_id": selected_verse["id"],
        "chapter_number": selected_verse["chapter_number"],
        "verse_number": selected_verse["verse_number"],
        "date": today
    }
    
    return verse_data

def update_verse_of_the_day():
    """
    Update the verse_of_the_day.json file with today's verse.
    """
    try:
        verse_data = get_verse_of_the_day()
        
        # Write to verse_of_the_day.json
        with open('verse_of_the_day.json', 'w', encoding='utf-8') as f:
            json.dump(verse_data, f, ensure_ascii=False, indent=2)
        
        print(f"Verse of the day updated for {verse_data['date']}")
        print(f"Chapter {verse_data['chapter_number']}, Verse {verse_data['verse_number']}")
        return True
        
    except Exception as e:
        print(f"Error updating verse of the day: {e}")
        return False

if __name__ == "__main__":
    update_verse_of_the_day() 