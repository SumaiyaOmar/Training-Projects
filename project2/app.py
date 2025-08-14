from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# ----------------------------
# Load JSON dataset
# ----------------------------
dataset = []

with open('asprs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def extract_chunks(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance (value, (dict,list)):
                extract_chunks(value)
            else:
                dataset.append(str(value))
    
    elif isinstance(obj,list):
        for item in obj:
            extract_chunks(item)

extract_chunks(data)

# ----------------------------
# Flask routes
# ----------------------------
@app.route("/")
def home():
    return render_template('chat.html')

@app.route("/ask", methods=['POST'])
def ask():
    message = str(request.form['messageText']).lower()
    # Search for matches in dataset
    matches = [chunk for chunk in dataset if message in chunk.lower() and len(chunk)>20]
    if matches:
        # Return first 3 matches (or all if less)
        return jsonify({'status':'OK','answer': '\n'.join(matches[:3])})
    else:
        return jsonify({'status':'OK','answer': "Sorry, I couldn't find anything."})

# ----------------------------
# Run Flask server
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
