from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import requests
from difflib import SequenceMatcher

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Requests from React frontend

# Load memory base and RAG data
with open("apikey.json", "r") as f:
    API_KEY = json.load(f)["apikey"]

with open("memory_base.json", "r") as f:
    memory_items = json.load(f)

with open("support_rag_dataset.json", "r", encoding="utf-8") as f:
    rag_data = json.load(f)

# Utility for matching
def find_best_match(user_input, rag_entries, top_n=1):
    def similarity(a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    scored = [(entry, similarity(user_input, entry["customer"])) for entry in rag_entries]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [s[0] for s in scored[:top_n]]

@app.route("/coach", methods=["POST"])
def coach():
    data = request.json
    customer_message = data.get("customer", "")
    agent_message = data.get("agent", "")

    # Get access token
    iam_url = "https://iam.cloud.ibm.com/identity/token"
    iam_data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }
    token_response = requests.post(iam_url, headers={"Content-Type": "application/x-www-form-urlencoded"}, data=iam_data)
    access_token = token_response.json()["access_token"]

    memory_text = "\n".join([
        f"""Trigger: "{item['trigger']}"
Emotion: {item['emotion']}
Advice: {item['advice']}
Tone: {item['tone']}
Cue: {item['cue']}\n""" for item in memory_items
    ])

    best_match = find_best_match(customer_message, rag_data)[0]

    prompt = f"""
You are Whispr.AI — an AI mentor that coaches support agents during live conversations. You do not speak to customers; you just coach the agent.
Instead of copying from memory, generate a **new coaching cue** tailored to the customer's message and emotional state. Use the tone and mindset from memory as guidance — not as a script.

Below is a similar past case retrieved from support logs for reference:
Customer: "{best_match['customer']}"
Agent: "{best_match['agent']}"

Memory Base (coaching guide):
{memory_text}

Now coach the agent in this new conversation:
Customer: "{customer_message}"
Agent: "{agent_message}"

Your output must include:
- Emotion detected
- Matching example trigger (if any)
- Agent mindset to adopt
- Suggested tone
- Coaching cue for next reply
"""

    # Send to watsonx ai
    response = requests.post(
        "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2024-05-01",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        json={
            "model_id": "ibm/granite-3-8b-instruct",
            "project_id": "30fac77c-eb4e-4742-9449-4815b0daeae6",
            "input": prompt,
            "parameters": {"decoding_method": "greedy", "max_new_tokens": 300}
        }
    )

    if response.status_code == 200:
        generated_text = response.json()["results"][0]["generated_text"]
        return jsonify({ "generated_text": generated_text })
    else:
        return jsonify({ "error": "AI model request failed", "details": response.text }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
