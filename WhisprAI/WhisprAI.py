import json
import requests
from difflib import SequenceMatcher

# Load API key
with open("apikey.json", "r") as f:
    data = json.load(f)
    API_KEY = data["apikey"]

# Load memory base
with open("memory_base.json", "r", encoding="utf-8") as f:
    memory_items = json.load(f)

# Load RAG dataset
with open("support_rag_dataset.json", "r", encoding="utf-8") as f:
    rag_data = json.load(f)

# Merge both into a common context list
context_examples = []
for entry in rag_data:
    context_examples.append({
        "source": "RAG",
        "customer": entry["customer"],
        "agent": entry["agent"],
        "emotion": None,
        "advice": None,
        "tone": None,
        "cue": None
    })

for entry in memory_items:
    context_examples.append({
        "source": "Memory",
        "customer": entry["trigger"],
        "agent": "",
        "emotion": entry["emotion"],
        "advice": entry["advice"],
        "tone": entry["tone"],
        "cue": entry["cue"]
    })

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

# STEP 2: Prepare the AI call
ai_url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2024-05-01"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}

# Utility function to find best match
def find_best_match(user_input, context_entries, top_n=1):
    def similarity(a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    scored = [(entry, similarity(user_input, entry["customer"])) for entry in context_entries]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [s[0] for s in scored[:top_n]]

# User input
print("🧠 Whispr.AI Coaching System")
customer_message = input("Enter the customer message: ")
agent_message = input("Enter the agent's reply: ")

# Retrieve best context from either dataset
best_context = find_best_match(customer_message, context_examples)[0]

# Construct the prompt
prompt = f"""
You are Whispr.AI — an AI mentor that coaches support agents during live conversations. You do not speak to customers; you just coach the agent.

Below is the most relevant support situation from your training data. Use it to understand both topic and emotional tone.

Customer: \"{best_context['customer']}\"
Agent: \"{best_context['agent']}\"
Source: {best_context['source']}
Emotion (if available): {best_context['emotion']}
Advice (if available): {best_context['advice']}
Tone (if available): {best_context['tone']}

Now coach the agent for the following live conversation:
Customer message: \"{customer_message}\"
Agent's current reply: \"{agent_message}\"

Instructions:
- Use the example to understand context, tone, and advice
- Write a new, emotionally appropriate coaching cue
- Do not copy any existing cue

Output format:
- Emotion detected:
- Matching example trigger:
- Agent mindset to adopt:
- Suggested tone:
- Coaching cue for next reply:
"""

# Payload
payload = {
    "model_id": "ibm/granite-3-8b-instruct",
    "project_id": "30fac77c-eb4e-4742-9449-4815b0daeae6",
    "input": prompt,
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
