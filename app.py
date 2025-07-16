from flask import Flask, request, jsonify, render_template, send_from_directory
from gita_bot import chain_krishna, chain_shloka, chain_explanation
from flask_cors import CORS

app = Flask(__name__, template_folder='.')
CORS(app)

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
    return render_template('Index.html')

@app.route('/Feather.png')
def feather_png():
    return send_from_directory('.', 'Feather.png')
    
if __name__ == '__main__':
    app.run(debug=True)
