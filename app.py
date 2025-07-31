from flask import Flask, request, jsonify, render_template, send_from_directory
from gita_bot import chain_krishna, chain_shloka, chain_explanation
from flask_cors import CORS
import json
import datetime
import os

app = Flask(__name__, template_folder='.')
CORS(app)

def should_update_verse_of_day():
    """
    Check if the verse of the day needs to be updated.
    Returns True if the verse is from a different date or doesn't exist.
    """
    try:
        if not os.path.exists('verse_of_the_day.json'):
            return True
        
        with open('verse_of_the_day.json', 'r', encoding='utf-8') as f:
            verse_data = json.load(f)
        
        # Check if the verse has a date field
        if 'date' not in verse_data:
            return True
        
        # Check if the date is today
        today = datetime.date.today().strftime('%Y-%m-%d')
        return verse_data['date'] != today
        
    except Exception:
        return True

def update_verse_of_day():
    """
    Update the verse of the day using the update script.
    """
    try:
        from update_verse_of_day import update_verse_of_the_day
        return update_verse_of_the_day()
    except Exception as e:
        print(f"Error updating verse of the day: {e}")
        return False

@app.route('/ask', methods=['POST'])
def ask_gita():
    data = request.get_json()
    question = data.get('question', '')
    if not question.strip():
        return jsonify({'error': 'No question provided.'}), 400
    
    try:
        # Get Krishna's wisdom
        wisdom = chain_krishna.invoke({"question": question})
        wisdom_text = wisdom.content if hasattr(wisdom, "content") else str(wisdom)

        # Get Shloka and translation
        shloka = chain_shloka.invoke({"question": question})
        shloka_text = shloka.content if hasattr(shloka, "content") else str(shloka)

        # Get Explanation
        explanation = chain_explanation.invoke({
            "question": question,
            "shloka_and_translation": shloka_text
        })
        explanation_text = explanation.content if hasattr(explanation, "content") else str(explanation)

        return jsonify({
            'wisdom': wisdom_text.strip(),
            'shloka': shloka_text.strip(),
            'explanation': explanation_text.strip()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/')
def landing():
    
    return render_template('Landing.html')

@app.route('/askgita')
def askgita():
    # Check if verse of the day needs to be updated
    if should_update_verse_of_day():
        update_verse_of_day()
    
    with open('verse_of_the_day.json', 'r', encoding='utf-8') as f:
        verse = json.load(f)
    return render_template('Index.html', verse=verse)

@app.route('/Feather.png')
def feather_png():
    return send_from_directory('.', 'Feather.png')

@app.route('/update-verse', methods=['POST'])
def update_verse_endpoint():
    """
    Manual endpoint to update the verse of the day.
    """
    try:
        success = update_verse_of_day()
        if success:
            with open('verse_of_the_day.json', 'r', encoding='utf-8') as f:
                verse = json.load(f)
            return jsonify({
                'success': True,
                'message': 'Verse of the day updated successfully',
                'verse': verse
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to update verse of the day'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating verse: {str(e)}'
        }), 500
    
if __name__ == '__main__':
    app.run(debug=True)
