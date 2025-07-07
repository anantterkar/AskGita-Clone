from flask import Flask, request, jsonify, render_template
from gita_bot import chain_general
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/ask', methods=['POST'])
def ask_gita():
    data = request.get_json()
    question = data.get('question', '')
    if not question.strip():
        return jsonify({'error': 'No question provided.'}), 400
    
    try:
        response = chain_general.invoke({"question": question})
        if isinstance(response, dict) and 'content' in response:
            main_response = response['content']
        elif hasattr(response, 'content'):
            main_response = response.content
        else:
            main_response = str(response)
        return jsonify({'answer': main_response.strip()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True)
