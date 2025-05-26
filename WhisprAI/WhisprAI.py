import json
import requests

# Load API key from JSON file
with open("apikey.json", "r") as f:
    data = json.load(f)
    API_KEY = data["apikey"]

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

# Whispr.AI memory base (you can expand this later)
memory_base = """
You are Whispr.AI — an AI mentor that coaches support agents during live conversations. You don't speak to customers; you coach the agent.

Use this memory base:
Trigger: “I’ve had to explain this multiple times.”
Emotion: Frustration + disbelief
Advice: Acknowledge their effort. Offer a new direction.
Tone: Focused, affirming
Cue: “I understand — and I appreciate your patience. I’ll take a different approach now.”

Trigger: “Why was I billed again?”
Emotion: Suspicion + confusion
Advice: Stay factual. Clarify without defensiveness.
Tone: Calm, professional
Cue: “Let me explain the charge and how we can resolve it if needed.”
"""

# User input
print("🧠 Whispr.AI Coaching System")
customer_message = input("Enter the customer message: ")
agent_message = input("Enter the agent's reply: ")

# Prompt to send
prompt = f"""
{memory_base}

Use the memory base only as reference. Do not generate new scenarios. Focus solely on the following conversation and provide coaching advice to the agent.

Customer: “{customer_message}”
Agent: “{agent_message}”

Your output must include only:
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
