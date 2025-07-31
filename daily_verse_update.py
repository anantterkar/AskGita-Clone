#!/usr/bin/env python3
"""
Daily Verse Update Script
This script updates the verse of the day and can be run as a scheduled task.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from update_verse_of_day import update_verse_of_the_day

def main():
    """
    Main function to update the verse of the day.
    """
    print("Starting daily verse update...")
    
    success = update_verse_of_the_day()
    
    if success:
        print("Daily verse update completed successfully!")
        sys.exit(0)
    else:
        print("Daily verse update failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 