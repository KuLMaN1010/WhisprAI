import json
import requests

# this is for loading API key from JSON file
with open("apikey.json", "r") as f:
    data = json.load(f)
    API_KEY = data["apikey"]

with open("memory_base.json", "r") as f:
    memory_items = json.load(f)

# Loading RAG dataset
with open("support_rag_dataset.json", "r", encoding="utf-8") as f:
    rag_data = json.load(f)


# STEP 1: Get the real access token
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
    print("❌ Failed to authenticate:", iam_response.status_code)
    print(iam_response.text)
    exit()

access_token = iam_response.json()["access_token"]

# STEP 2: Use token to call watsonx.ai
ai_url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2024-05-01"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}

# Whispr.AI memory base
# Dynamically build memory base text for prompt
memory_base_text = "\n".join([
    f"""Trigger: "{item['trigger']}"
Emotion: {item['emotion']}
Advice: {item['advice']}
Tone: {item['tone']}
Cue: {item['cue']}\n""" for item in memory_items
])

from difflib import SequenceMatcher

def find_best_match(user_input, rag_entries, top_n=1):
    def similarity(a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    scored = [
        (entry, similarity(user_input, entry["customer"]))
        for entry in rag_entries
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [s[0] for s in scored[:top_n]]


# User input
print("🧠 Whispr.AI Coaching System")
customer_message = input("Enter the customer message: ")
agent_message = input("Enter the agent's reply: ")

# Get most similar past case from RAG dataset
best_match = find_best_match(customer_message, rag_data)[0]


# Prompt to send to watsonx.ai
prompt = f"""
You are Whispr.AI — an AI mentor that coaches support agents during live conversations. You do not speak to customers; you just coach the agent.

Below is a similar past case retrieved from support logs:
Customer: "{best_match['customer']}"
Agent: "{best_match['agent']}"

Memory Base (coaching guide):
{memory_base_text}

Now coach the agent in this new conversation:
Customer: "{customer_message}"
Agent: "{agent_message}"

Your output must include:
- Emotion detected
- Matching coaching memory item
- Agent mindset to adopt
- Suggested tone
- Coaching cue for next reply
"""

# Payload
payload = {
    "model_id": "ibm/granite-3-8b-instruct",
    "project_id": "30fac77c-eb4e-4742-9449-4815b0daeae6",
    "input": prompt,  # ✅ this is your full prompt
    "parameters": {
        "decoding_method": "greedy",
        "max_new_tokens": 300
    }
}



# Final request to AI model
response = requests.post(ai_url, headers=headers, json=payload)

# Output result
if response.status_code == 200:
    result = response.json()
    print("\n🔹 Whispr.AI Coaching Response 🔹")
    print(result["results"][0]["generated_text"])
else:
    print("❌ Error:", response.status_code)
    print(response.text)
