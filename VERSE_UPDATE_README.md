# Daily Verse Update System

This system automatically updates the verse of the day each day, ensuring users see a fresh verse from the Bhagavad Gita.

## How It Works

1. **Daily Selection**: The system uses the current date as a seed to select a random verse from the complete Bhagavad Gita dataset (`verse.json`).

2. **Consistent Daily Results**: Using the date as a seed ensures that:
   - The same verse is selected for the same date across different runs
   - Different verses are selected for different dates
   - The selection is deterministic and reproducible

3. **Automatic Updates**: The verse is automatically updated when:
   - The application starts and detects the current verse is from a different date
   - The `/askgita` route is accessed and the verse needs updating
   - The manual update endpoint `/update-verse` is called

## Files

- `update_verse_of_day.py`: Main script for updating the verse of the day
- `daily_verse_update.py`: Standalone script for scheduled tasks
- `verse_of_the_day.json`: Contains the current verse of the day
- `verse.json`: Complete dataset of all Bhagavad Gita verses

## Usage

### Manual Update
```bash
python update_verse_of_day.py
```

### Scheduled Task (Windows)
1. Open Task Scheduler
2. Create a new Basic Task
3. Set trigger to daily at your preferred time
4. Set action to start a program: `python`
5. Add arguments: `daily_verse_update.py`
6. Set start in: `C:\Users\adibr\Desktop\AskGita`

### Scheduled Task (Linux/Mac)
Add to crontab:
```bash
# Update verse daily at 6 AM
0 6 * * * cd /path/to/AskGita && python daily_verse_update.py
```

### API Endpoint
```bash
curl -X POST http://localhost:5000/update-verse
```

## Verse Data Structure

The updated `verse_of_the_day.json` contains:
```json
{
  "text": "Sanskrit verse text",
  "translation": "English translation",
  "verse_id": 28,
  "chapter_number": 1,
  "verse_number": 28,
  "transliteration": "Romanized Sanskrit",
  "date": "2025-07-31"
}
```

## Integration

The system is integrated into the Flask app (`app.py`):
- Automatically checks if verse needs updating when `/askgita` is accessed
- Provides manual update endpoint at `/update-verse`
- Maintains backward compatibility with existing code

## Benefits

1. **Fresh Content**: Users see a new verse each day
2. **Consistent Experience**: Same verse for same date across sessions
3. **Automatic**: No manual intervention required
4. **Reliable**: Uses deterministic selection based on date
5. **Flexible**: Can be updated manually or automatically 