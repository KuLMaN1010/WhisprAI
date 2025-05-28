from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/coach', methods=['POST'])
def coach():
    data = request.json
    customer = data.get("customer", "")
    agent = data.get("agent", "")

    # TEMP: Replace this with real logic from your coaching system
    response = {
        "emotion": "Calm + confusion",
        "trigger": "Billing issue",
        "mindset": "Empathetic + clear",
        "tone": "Professional",
        "cue": f"Hi! Regarding '{customer}', reassure and explain the issue clearly. Avoid blame."
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
