from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import requests
from difflib import SequenceMatcher

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load API key
with open("apikey.json", "r") as f:
    API_KEY = json.load(f)["apikey"]

# Load memory base and RAG dataset
with open("memory_base.json", "r", encoding="utf-8") as f:
    memory_items = json.load(f)

with open("support_rag_dataset.json", "r", encoding="utf-8") as f:
    rag_data = json.load(f)

# Prepare memory base text for prompt
memory_base_text = "\n".join([
    f"""Trigger: "{item['trigger']}"
Emotion: {item['emotion']}
Advice: {item['advice']}
Tone: {item['tone']}
Cue: {item['cue']}\n""" for item in memory_items
])

# Function to find closest customer match from RAG
def find_best_match(user_input, rag_entries, top_n=1):
    def similarity(a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    scored = [
        (entry, similarity(user_input, entry["customer"]))
        for entry in rag_entries
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [s[0] for s in scored[:top_n]]

@app.route('/api/coach', methods=['POST'])
def coach():
    data = request.json
    customer = data.get("customer", "")
    agent = data.get("agent", "")

    # Get best match from RAG data
    best_match = find_best_match(customer, rag_data)[0]

    # Get IAM access token
    iam_url = "https://iam.cloud.ibm.com/identity/token"
    iam_headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    iam_data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }
    iam_response = requests.post(iam_url, headers=iam_headers, data=iam_data)

    if iam_response.status_code != 200:
        return jsonify({"error": "Authentication with IBM failed."}), 500

    access_token = iam_response.json()["access_token"]

    # Prompt
    prompt = f"""
You are Whispr.AI — an AI mentor that coaches support agents during live conversations.
You do not speak to customers directly.

Use the coaching memory and support examples to guide your suggestions.
Your job is to detect emotion, match a similar coaching example, suggest the agent's mindset, tone, and give a **clear, specific coaching cue** that helps the agent sound professional and empathetic.

Do NOT copy the customer's message into your cue.
Do NOT reuse cue text from memory word-for-word.
Do NOT repeat the customer's words.

Here is a similar past case:
Customer: "{best_match['customer']}"
Agent: "{best_match['agent']}"

Coaching Memory Base:
{memory_base_text}

Now coach the agent:
Customer: "{customer}"
Agent: "{agent}"

Your response must include:
- Emotion detected
- Matching example trigger
- Agent mindset to adopt
- Suggested tone
- Coaching cue for next reply
"""

    # AI request
    ai_url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2024-05-01"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "model_id": "ibm/granite-3-8b-instruct",
        "project_id": "30fac77c-eb4e-4742-9449-4815b0daeae6",
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 300
        }
    }

    ai_response = requests.post(ai_url, headers=headers, json=payload)

    if ai_response.status_code != 200:
        return jsonify({"error": "Failed to get response from AI"}), 500

    result_text = ai_response.json()["results"][0]["generated_text"]
    return jsonify(parse_ai_response(result_text))

# Parse AI response text into structured JSON
def parse_ai_response(text):
    result = {
        "emotion": "",
        "trigger": "",
        "mindset": "",
        "tone": "",
        "cue": ""
    }

    for line in text.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip().lower()
            val = val.strip()
            if "emotion" in key:
                result["emotion"] = val
            elif "trigger" in key:
                result["trigger"] = val
            elif "mindset" in key:
                result["mindset"] = val
            elif "tone" in key:
                result["tone"] = val
            elif "cue" in key:
                result["cue"] = val

    return result

if __name__ == "__main__":
    app.run(port=5000, debug=True)
